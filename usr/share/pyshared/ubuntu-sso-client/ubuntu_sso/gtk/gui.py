# -*- coding: utf-8 -*-
#
# Copyright 2010-2012 Canonical Ltd.
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License version 3, as published
# by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranties of
# MERCHANTABILITY, SATISFACTORY QUALITY, or FITNESS FOR A PARTICULAR
# PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# In addition, as a special exception, the copyright holders give
# permission to link the code of portions of this program with the
# OpenSSL library under certain conditions as described in each
# individual source file, and distribute linked combinations
# including the two.
# You must obey the GNU General Public License in all respects
# for all of the code used other than OpenSSL.  If you modify
# file(s) with this exception, you may extend this exception to your
# version of the file(s), but you are not obligated to do so.  If you
# do not wish to do so, delete this exception statement from your
# version.  If you delete this exception statement from all source
# files in the program, then also delete it here.
"""User registration GUI."""

import logging
import os
import sys
import tempfile
import webbrowser

from functools import wraps, partial

# pylint: disable=E0611,F0401
from gi.repository import Gdk, Gtk
from gi.repository.GdkX11 import X11Window
# pylint: enable=E0611,F0401
from twisted.internet import defer

from ubuntu_sso import (
    main,
    NO_OP,
    USER_CANCELLATION,
    USER_SUCCESS,
    utils,
)
from ubuntu_sso.logger import setup_gui_logging
from ubuntu_sso.utils import get_data_file
from ubuntu_sso.utils.ui import (
    CAPTCHA_LOAD_ERROR,
    CAPTCHA_RELOAD_TOOLTIP,
    CONNECT_HELP_LABEL,
    EMAIL_MISMATCH,
    EMAIL_INVALID,
    ERROR,
    FIELD_REQUIRED,
    FORGOTTEN_PASSWORD_BUTTON,
    GENERIC_BACKEND_ERROR,
    is_min_required_password,
    is_correct_email,
    JOIN_HEADER_LABEL,
    LOADING,
    LOGIN_BUTTON_LABEL,
    LOGIN_HEADER_LABEL,
    NEXT,
    ONE_MOMENT_PLEASE,
    PASSWORD_CHANGED,
    PASSWORD_HELP,
    PASSWORD_MISMATCH,
    PASSWORD_TOO_WEAK,
    REQUEST_PASSWORD_TOKEN_LABEL,
    RESET_PASSWORD,
    SET_NEW_PASSWORD_LABEL,
    SUCCESS,
    TC_BUTTON,
    TC_NOT_ACCEPTED,
    VERIFY_EMAIL_LABEL,
    YES_TO_TC,
    YES_TO_UPDATES,
)


# Instance of 'UbuntuSSOClientGUI' has no 'yyy' member
# pylint: disable=E1101


logger = setup_gui_logging('ubuntu_sso.gui.gtk')


# pylint: disable=C0103
def parse_color(color):
    """Parse a string color into Gdk.Color."""
    c = Gdk.RGBA()
    result = c.parse(color)
    if not result:
        logger.warning('Could not parse color %r.', color)
    return c
# pylint: enable=C0103

DEFAULT_WIDTH = 30
# To be replaced by values from the theme (LP: #616526)
HELP_TEXT_COLOR = parse_color("#bfbfbf")
WARNING_TEXT_COLOR = parse_color("red")
LARGE_MARKUP = u'<span size="x-large">%s</span>'


# SSL properties and certs location
STRICT_SSL_PROP = 'ssl-strict'
CERTS_FILE_PROP = 'ssl-ca-file'
CA_CERT_FILE = '/etc/ssl/certs/ca-certificates.crt'


def log_call(f):
    """Decorator to log call funtions."""

    @wraps(f)
    def inner(*args, **kwargs):
        """Execute 'f' logging the call as INFO."""
        logger.info('%s: args %r, kwargs %r.', f.__name__, args, kwargs)
        return f(*args, **kwargs)

    return inner


class LabeledEntry(Gtk.Entry):
    """An entry that displays the label within itself ina grey color."""

    # Use of super on an old style class
    # pylint: disable=E1002

    def __init__(self, label, is_password=False, *args, **kwargs):
        self.label = label
        self.is_password = is_password
        self.warning = None

        super(LabeledEntry, self).__init__(*args, **kwargs)

        self.set_width_chars(DEFAULT_WIDTH)
        self._set_label(self, None)
        self.set_tooltip_text(self.label)
        self.connect('focus-in-event', self._clear_text)
        self.connect('focus-out-event', self._set_label)
        self.clear_warning()
        self.show()

    def _clear_text(self, *args, **kwargs):
        """Clear text and restore text color."""
        self.set_text(self.get_text())

        # restore to theme's default
        self.override_color(Gtk.StateFlags.NORMAL, None)

        if self.is_password:
            self.set_visibility(False)

        return False  # propagate the event further

    def _set_label(self, *args, **kwargs):
        """Set the proper label and proper coloring."""
        if self.get_text():
            return

        self.set_text(self.label)
        self.override_color(Gtk.StateFlags.NORMAL, HELP_TEXT_COLOR)

        if self.is_password:
            self.set_visibility(True)

        return False  # propagate the event further

    def get_text(self):
        """Get text only if it's not the label nor empty."""
        result = super(LabeledEntry, self).get_text().decode('utf8')
        if result == self.label or result.isspace():
            result = u''
        return result

    def set_warning(self, warning_msg):
        """Display warning as secondary icon, set 'warning_msg' as tooltip."""
        self.warning = warning_msg
        self.set_property('secondary-icon-stock', Gtk.STOCK_DIALOG_WARNING)
        self.set_property('secondary-icon-sensitive', True)
        self.set_property('secondary-icon-activatable', False)
        self.set_property('secondary-icon-tooltip-text', warning_msg)

    def clear_warning(self):
        """Remove any warning."""
        self.warning = None
        self.set_property('secondary-icon-stock', None)
        self.set_property('secondary-icon-sensitive', False)
        self.set_property('secondary-icon-activatable', False)
        self.set_property('secondary-icon-tooltip-text', None)


class UbuntuSSOClientGUI(object):
    """Ubuntu single sign-on GUI."""

    def __init__(self, app_name, **kwargs):
        """Create the GUI and initialize widgets."""
        logger.debug('UbuntuSSOClientGUI: app_name %r, kwargs %r.',
                     app_name, kwargs)

        self._captcha_filename = tempfile.mktemp()
        self._captcha_id = None
        self._signals_receivers = {}
        self._done = False  # whether the whole process was completed or not

        self.app_name = app_name
        self.app_label = u'<b>%s</b>' % self.app_name
        self.ping_url = kwargs.get('ping_url', u'')
        self.tc_url = kwargs.get('tc_url', u'')
        self.help_text = kwargs.get('help_text', u'')
        self.login_only = kwargs.get('login_only', False)
        window_id = kwargs.get('window_id', 0)
        self.close_callback = kwargs.get('close_callback', NO_OP)
        self.backend = None
        self.user_email = None
        self.user_password = None

        ui_filename = get_data_file('gtk', 'ui.glade')
        builder = Gtk.Builder()
        builder.add_from_file(ui_filename)
        builder.connect_signals(self)

        self.widgets = []
        self.warnings = []
        self.cancels = []
        for obj in builder.get_objects():
            name = getattr(obj, 'name', None)
            if name is None and isinstance(obj, Gtk.Buildable):
                # work around bug lp:507739
                name = Gtk.Buildable.get_name(obj)
            if name is None:
                logging.warn("%s has no name (??)", obj)
            else:
                self.widgets.append(name)
                setattr(self, name, obj)
                if 'warning' in name:
                    self.warnings.append(obj)
                    obj.set_text('')
                if 'cancel_button' in name:
                    obj.connect('clicked', self.on_close_clicked)
                    self.cancels.append(obj)

        # Connect the activate-link signal here
        # GtkBuilder in GTK 3 seems to not do this
        self.login_button.connect('activate-link', self.on_activate_link)
        self.forgotten_password_button.connect('activate-link',
                                               self.on_activate_link)

        self.entries = (u'name_entry', u'email1_entry', u'email2_entry',
                        u'password1_entry', u'password2_entry',
                        u'captcha_solution_entry', u'email_token_entry',
                        u'login_email_entry', u'login_password_entry',
                        u'reset_email_entry', u'reset_code_entry',
                        u'reset_password1_entry', u'reset_password2_entry')

        for name in self.entries:
            label = getattr(utils.ui, name.upper())
            is_password = 'password' in name
            entry = LabeledEntry(label=label, is_password=is_password)
            entry.set_activates_default(True)
            setattr(self, name, entry)

        self.window.set_icon_name('ubuntu-logo')

        self.pages = (self.enter_details_vbox, self.processing_vbox,
                      self.verify_email_vbox, self.finish_vbox,
                      self.tc_browser_vbox, self.login_vbox,
                      self.request_password_token_vbox,
                      self.set_new_password_vbox)

        self._signals = {
            'CaptchaGenerated':
             self._filter_by_app_name(self.on_captcha_generated),
            'CaptchaGenerationError':
             self._filter_by_app_name(self.on_captcha_generation_error),
            'UserRegistered':
             self._filter_by_app_name(self.on_user_registered),
            'UserRegistrationError':
             self._filter_by_app_name(self.on_user_registration_error),
            'EmailValidated':
             self._filter_by_app_name(self.on_email_validated),
            'EmailValidationError':
             self._filter_by_app_name(self.on_email_validation_error),
            'LoggedIn':
             self._filter_by_app_name(self.on_logged_in),
            'LoginError':
             self._filter_by_app_name(self.on_login_error),
            'UserNotValidated':
             self._filter_by_app_name(self.on_user_not_validated),
            'PasswordResetTokenSent':
             self._filter_by_app_name(self.on_password_reset_token_sent),
            'PasswordResetError':
             self._filter_by_app_name(self.on_password_reset_error),
            'PasswordChanged':
             self._filter_by_app_name(self.on_password_changed),
            'PasswordChangeError':
             self._filter_by_app_name(self.on_password_change_error),
        }

        if window_id != 0:
            # be as robust as possible:
            # if the window_id is not "good", set_transient_for will fail
            # awfully, and we don't want that: if the window_id is bad we can
            # still do everything as a standalone window. Also,
            # window_foreign_new may return None breaking set_transient_for.
            try:
                display = Gdk.Display.get_default()
                # this is not working, we need to create a XLib.window
                # as a second parameter to foreign_new_for_display
                win = X11Window.foreign_new_for_display(display, None)
                self.window.realize()
                self.window.window.set_transient_for(win)
            except:  # pylint: disable=W0702
                msg = 'UbuntuSSOClientGUI: failed set_transient_for win id %r'
                logger.exception(msg, window_id)

        self.yes_to_updates_checkbutton.hide()
        self.start_backend()

    @defer.inlineCallbacks
    def start_backend(self):
        """Start the backend, show the window when ready."""
        client = yield main.get_sso_client()
        self.backend = client.sso_login

        logger.debug('UbuntuSSOClientGUI: backend created: %r', self.backend)

        self._setup_signals()
        self._append_pages()
        self.window.show()

    @property
    def success_vbox(self):
        """The success page."""
        message = SUCCESS % {'app_name': self.app_name}
        message = LARGE_MARKUP % message
        self.finish_vbox.label.set_markup(message)
        return self.finish_vbox

    @property
    def error_vbox(self):
        """The error page."""
        self.finish_vbox.label.set_markup(LARGE_MARKUP % ERROR)
        return self.finish_vbox

    # helpers

    def _filter_by_app_name(self, f):
        """Excecute the decorated function only for 'self.app_name'."""

        @wraps(f)
        def inner(app_name, *args, **kwargs):
            """Execute 'f' only if 'app_name' matches 'self.app_name'."""
            result = None
            if app_name == self.app_name:
                result = f(app_name, *args, **kwargs)
            else:
                logger.info('%s: ignoring call since received app_name '\
                            '%r (expected %r)',
                            f.__name__, app_name, self.app_name)
            return result

        return inner

    def _setup_signals(self):
        """Bind signals to callbacks to be able to test the pages."""
        for signal, method in self._signals.iteritems():
            actual = self._signals_receivers.get(signal)
            if actual is not None:
                msg = 'Signal %r is already connected with %r.'
                logger.warning(msg, signal, actual)

            match = self.backend.connect_to_signal(signal, method)
            self._signals_receivers[signal] = match

    def _add_spinner_to_container(self, container, legend=None):
        """Add a spinner to 'container'."""
        spinner = Gtk.Spinner()
        spinner.start()

        label = Gtk.Label()
        if legend:
            label.set_text(legend)
        else:
            label.set_text(LOADING)

        hbox = Gtk.HBox(spacing=5)
        hbox.pack_start(spinner, expand=False, fill=True, padding=0)
        hbox.pack_start(label, expand=False, fill=True, padding=0)

        alignment = Gtk.Alignment(xalign=0.5, yalign=0.5,
                                  xscale=0, yscale=0)
        alignment.add(hbox)
        alignment.show_all()

        # remove children to avoid:
        # GtkWarning: Attempting to add a widget with type GtkAlignment to a
        # GtkEventBox, but as a GtkBin subclass a GtkEventBox can only contain
        # one widget at a time
        for child in container.get_children():
            container.remove(child)
        container.add(alignment)

    def _set_warning_message(self, widget, message):
        """Set 'message' as text for 'widget'."""
        widget.set_text(message)
        widget.override_color(Gtk.StateFlags.NORMAL, WARNING_TEXT_COLOR)
        widget.show()

    def _clear_warnings(self):
        """Clear all warning messages."""
        for widget in self.warnings:
            widget.set_text('')
        for widget in self.entries:
            getattr(self, widget).clear_warning()

    def _non_empty_input(self, widget):
        """Return weather widget has non empty content."""
        text = widget.get_text()
        return bool(text and not text.isspace())

    def _handle_error(self, remote_call, handler, error):
        """Handle any error when calling the remote backend."""
        logger.error('Remote call %r failed with: %r', remote_call, error)
        errordict = {'message': GENERIC_BACKEND_ERROR}
        handler(self.app_name, errordict)

    # build pages

    def _append_pages(self):
        """Append all the requires pages to main widget."""
        self._append_page(self._build_processing_page())
        self._append_page(self._build_finish_page())
        self._append_page(self._build_login_page())
        self._append_page(self._build_request_password_token_page())
        self._append_page(self._build_set_new_password_page())
        self._append_page(self._build_verify_email_page())

        if not self.login_only:
            self._append_page(self._build_enter_details_page())
            self._append_page(self._build_tc_page())
            self.login_button.grab_focus()
            self._set_current_page(self.enter_details_vbox)
        else:
            self.login_back_button.hide()
            self.login_ok_button.grab_focus()
            self.login_vbox.help_text = self.help_text
            self._set_current_page(self.login_vbox)

    def _append_page(self, page):
        """Append 'page' to the 'window'."""
        self.content.append_page(page, None)

    def _set_header(self, header):
        """Set 'header' as the window title and header."""
        self.header_label.set_markup(LARGE_MARKUP % header)
        self.window.set_title(self.header_label.get_text())  # avoid markup

    def _set_current_page(self, current_page, warning_text=None):
        """Hide all the pages but 'current_page'."""
        if hasattr(current_page, 'header'):
            self._set_header(current_page.header)

        if hasattr(current_page, 'help_text'):
            self.help_label.set_markup(current_page.help_text)

        if warning_text is not None:
            self._set_warning_message(self.warning_label, warning_text)
        else:
            self.warning_label.set_text('')

        self.content.set_current_page(self.content.page_num(current_page))

        if current_page.default_widget is not None:
            current_page.default_widget.grab_default()

    def _generate_captcha(self):
        """Ask for a new captcha; update the ui to reflect the fact."""
        logger.info('Calling generate_captcha with filename path at %r',
                    self._captcha_filename)
        self.warning_label.set_text('')
        f = self.backend.generate_captcha
        error_handler = partial(self._handle_error, f,
                                self.on_captcha_generation_error)
        f(self.app_name, self._captcha_filename,
            reply_handler=NO_OP, error_handler=error_handler)
        self._set_captcha_loading()

    def _set_captcha_loading(self):
        """Present a spinner to the user while the captcha is downloaded."""
        self.captcha_image.hide()
        self._add_spinner_to_container(self.captcha_loading)
        self.captcha_loading.override_background_color(Gtk.StateFlags.NORMAL,
                                                       parse_color('white'))
        self.captcha_loading.show_all()
        self.join_ok_button.set_sensitive(False)

    def _set_captcha_image(self):
        """Present a captcha image to the user to be resolved."""
        self.captcha_loading.hide()
        self.join_ok_button.set_sensitive(True)
        self.captcha_image.set_from_file(self._captcha_filename)
        self.captcha_image.show()

    def _build_enter_details_page(self):
        """Build the enter details page."""
        d = {'app_name': self.app_label}
        self.enter_details_vbox.header = JOIN_HEADER_LABEL % d
        self.enter_details_vbox.help_text = self.help_text
        self.enter_details_vbox.default_widget = self.join_ok_button
        self.join_ok_button.set_can_default(True)

        self.enter_details_vbox.pack_start(self.name_entry,
            expand=False, fill=True, padding=0)
        self.enter_details_vbox.reorder_child(self.name_entry, 0)
        entry = self.captcha_solution_entry
        self.captcha_solution_vbox.pack_start(entry,
            expand=False, fill=True, padding=0)
        msg = CAPTCHA_RELOAD_TOOLTIP
        self.captcha_reload_button.set_tooltip_text(msg)

        self.emails_hbox.pack_start(self.email1_entry,
            expand=False, fill=True, padding=0)
        self.emails_hbox.pack_start(self.email2_entry,
            expand=False, fill=True, padding=0)

        self.passwords_hbox.pack_start(self.password1_entry,
            expand=False, fill=True, padding=0)
        self.passwords_hbox.pack_start(self.password2_entry,
            expand=False, fill=True, padding=0)
        help_msg = '<small>%s</small>' % PASSWORD_HELP
        self.password_help_label.set_markup(help_msg)

        if not os.path.exists(self._captcha_filename):
            self._generate_captcha()
        else:
            self._set_captcha_image()

        msg = YES_TO_UPDATES % {'app_name': self.app_name}
        self.yes_to_updates_checkbutton.set_label(msg)

        msg = YES_TO_TC % {'app_name': self.app_name}
        self.yes_to_tc_checkbutton.set_label(msg)
        self.tc_button.set_label(TC_BUTTON)

        if not self.tc_url:
            self.tc_vbox.hide()
        self.login_button.set_label(LOGIN_BUTTON_LABEL)

        return self.enter_details_vbox

    def _build_tc_page(self):
        """Build the Terms & Conditions page."""
        self.tc_browser_vbox.help_text = ''
        self.tc_browser_vbox.default_widget = self.tc_back_button
        self.tc_browser_vbox.default_widget.set_can_default(True)
        return self.tc_browser_vbox

    def _build_processing_page(self):
        """Build the processing page with a spinner."""
        self.processing_vbox.default_widget = None
        self._add_spinner_to_container(self.processing_vbox,
                                       legend=ONE_MOMENT_PLEASE)
        return self.processing_vbox

    def _build_verify_email_page(self):
        """Build the verify email page."""
        self.verify_email_vbox.default_widget = self.verify_token_button
        self.verify_email_vbox.default_widget.set_can_default(True)

        self.verify_email_details_vbox.pack_start(self.email_token_entry,
            expand=False, fill=True, padding=0)
        return self.verify_email_vbox

    def _build_finish_page(self):
        """Build the success page."""
        self.finish_vbox.default_widget = self.finish_close_button
        self.finish_vbox.default_widget.set_can_default(True)
        self.finish_vbox.label = self.finish_label
        return self.finish_vbox

    def _build_login_page(self):
        """Build the login page."""
        d = {'app_name': self.app_label}
        self.login_vbox.header = LOGIN_HEADER_LABEL % d
        self.login_vbox.help_text = CONNECT_HELP_LABEL % d
        self.login_vbox.default_widget = self.login_ok_button
        self.login_vbox.default_widget.set_can_default(True)

        self.login_details_vbox.pack_start(self.login_email_entry,
            expand=True, fill=True, padding=0)
        self.login_details_vbox.reorder_child(self.login_email_entry, 0)
        self.login_details_vbox.pack_start(self.login_password_entry,
            expand=True, fill=True, padding=0)
        self.login_details_vbox.reorder_child(self.login_password_entry, 1)

        msg = FORGOTTEN_PASSWORD_BUTTON
        self.forgotten_password_button.set_label(msg)
        self.login_ok_button.grab_focus()

        return self.login_vbox

    def _build_request_password_token_page(self):
        """Build the login page."""
        self.request_password_token_vbox.header = RESET_PASSWORD
        text = REQUEST_PASSWORD_TOKEN_LABEL % {'app_name': self.app_label}
        self.request_password_token_vbox.help_text = text
        btn = self.request_password_token_ok_button
        btn.set_can_default(True)
        self.request_password_token_vbox.default_widget = btn

        entry = self.reset_email_entry
        self.request_password_token_details_vbox.pack_start(entry,
            expand=False, fill=True, padding=0)
        cb = self.on_reset_email_entry_changed
        self.reset_email_entry.connect('changed', cb)
        self.request_password_token_ok_button.set_label(NEXT)
        self.request_password_token_ok_button.set_sensitive(False)

        return self.request_password_token_vbox

    def _build_set_new_password_page(self):
        """Build the login page."""
        self.set_new_password_vbox.header = RESET_PASSWORD
        self.set_new_password_vbox.help_text = SET_NEW_PASSWORD_LABEL
        btn = self.set_new_password_ok_button
        btn.set_can_default(True)
        self.set_new_password_vbox.default_widget = btn

        for entry in (self.reset_code_entry,
                      self.reset_password1_entry,
                      self.reset_password2_entry):
            self.set_new_password_details_vbox.pack_start(entry,
                expand=False, fill=True, padding=0)

        cb = self.on_set_new_password_entries_changed
        self.reset_code_entry.connect('changed', cb)
        self.reset_password1_entry.connect('changed', cb)
        self.reset_password2_entry.connect('changed', cb)
        help_msg = '<small>%s</small>' % PASSWORD_HELP
        self.reset_password_help_label.set_markup(help_msg)

        self.set_new_password_ok_button.set_label(RESET_PASSWORD)
        self.set_new_password_ok_button.set_sensitive(False)

        return self.set_new_password_vbox

    def _validate_email(self, email1, email2=None):
        """Validate 'email1', return error message if not valid.

        If 'email2' is given, must match 'email1'.
        """
        if email2 is not None and email1 != email2:
            return EMAIL_MISMATCH

        if not email1:
            return FIELD_REQUIRED

        if not is_correct_email(email1):
            return EMAIL_INVALID

    def _validate_password(self, password1, password2=None):
        """Validate 'password1', return error message if not valid.

        If 'password2' is given, must match 'email1'.
        """
        if password2 is not None and password1 != password2:
            return PASSWORD_MISMATCH

        if not is_min_required_password(password1):
            return PASSWORD_TOO_WEAK

    # GTK callbacks

    def destroy(self):
        """Destroy this UI."""
        self.window.hide()
        self.window.destroy()

    def connect(self, signal_name, handler, *args, **kwargs):
        """Connect 'signal_name' with 'handler'."""
        logger.debug('connect: signal %r, handler %r, args  %r, kwargs, %r',
                     signal_name, handler, args, kwargs)
        self.window.connect(signal_name, handler, *args, **kwargs)

    def finish_success(self):
        """The whole process was completed succesfully. Show success page."""
        self._done = True
        self._set_current_page(self.success_vbox)

    def finish_error(self):
        """The whole process was not completed succesfully. Show error page."""
        self._done = True
        self._set_current_page(self.error_vbox)

    def on_activate_link(self, button):
        """Do nothing, used for LinkButtons that are used as regular ones."""
        return True

    def on_close_clicked(self, *args, **kwargs):
        """Call self.close_callback if defined."""
        if os.path.exists(self._captcha_filename):
            os.remove(self._captcha_filename)

        for signal, match in self._signals_receivers.iteritems():
            self.backend.disconnect_from_signal(signal, match)

        # hide the main window
        if self.window is not None:
            self.window.hide()

        # process any pending events before callbacking with result
        while Gtk.events_pending():
            Gtk.main_iteration()

        return_code = USER_SUCCESS
        if not self._done:
            return_code = USER_CANCELLATION
        logger.info('Return code will be %r.', return_code)

        # call user defined callback
        logger.debug('Calling custom close_callback %r with params %r, %r',
                    self.close_callback, args, kwargs)
        self.close_callback(*args, **kwargs)

        sys.exit(return_code)

    def on_sign_in_button_clicked(self, *args, **kwargs):
        """User wants to sign in, present the Login page."""
        self._set_current_page(self.login_vbox)

    def on_join_ok_button_clicked(self, *args, **kwargs):
        """Submit info for processing, present the processing vbox."""
        if not self.join_ok_button.is_sensitive():
            return

        self._clear_warnings()

        error = False

        name = self.name_entry.get_text()
        if not name:
            self.name_entry.set_warning(FIELD_REQUIRED)
            logger.warning('on_join_ok_button_clicked: name not set.')
            error = True

        # check email
        email1 = self.email1_entry.get_text()
        email2 = self.email2_entry.get_text()
        msg = self._validate_email(email1, email2)
        if msg is not None:
            self.email1_entry.set_warning(msg)
            self.email2_entry.set_warning(msg)
            logger.warning('on_join_ok_button_clicked: email is not valid.')
            error = True

        # check password
        password1 = self.password1_entry.get_text()
        password2 = self.password2_entry.get_text()
        msg = self._validate_password(password1, password2)
        if msg is not None:
            self.password1_entry.set_warning(msg)
            self.password2_entry.set_warning(msg)
            logger.warning('on_join_ok_button_clicked: password is not valid.')
            error = True

        # check T&C
        if self.tc_url and not self.yes_to_tc_checkbutton.get_active():
            self._set_warning_message(self.tc_warning_label,
                TC_NOT_ACCEPTED % {'app_name': self.app_name})
            logger.warning('on_join_ok_button_clicked: terms and conditions '
                           'not accepted.')
            error = True

        captcha_solution = self.captcha_solution_entry.get_text()
        if not captcha_solution:
            self.captcha_solution_entry.set_warning(FIELD_REQUIRED)
            logger.warning('on_join_ok_button_clicked: captcha solution not '
                           'set.')
            error = True

        if error:
            logger.warning('on_join_ok_button_clicked: validation failed.')
            return

        logger.info('on_join_ok_button_clicked: validation success!')

        self._set_current_page(self.processing_vbox)
        self.user_email = email1
        self.user_password = password1

        logger.info('Calling register_user with email %r, password <hidden>,' \
                    ' name %r, captcha_id %r and captcha_solution %r.', email1,
                    name, self._captcha_id, captcha_solution)

        f = self.backend.register_user
        error_handler = partial(self._handle_error, f,
                                self.on_user_registration_error)
        f(self.app_name, self.user_email, self.user_password, name,
          self._captcha_id, captcha_solution,
          reply_handler=NO_OP, error_handler=error_handler)

    def on_verify_token_button_clicked(self, *args, **kwargs):
        """The user entered the email token, let's verify!"""
        if not self.verify_token_button.is_sensitive():
            return

        self._clear_warnings()

        email_token = self.email_token_entry.get_text()
        if not email_token:
            self.email_token_entry.set_warning(FIELD_REQUIRED)
            return

        email = self.user_email
        password = self.user_password

        args = (self.app_name, email, password, email_token)
        if self.ping_url:
            f = self.backend.validate_email_and_ping
            args = args + (self.ping_url,)
        else:
            f = self.backend.validate_email

        logger.info('Calling validate_email with email %r, password <hidden>, '
                    'app_name %r and email_token %r.', email, self.app_name,
                    email_token)
        error_handler = partial(self._handle_error, f,
                                self.on_email_validation_error)
        f(*args, reply_handler=NO_OP, error_handler=error_handler)

        self._set_current_page(self.processing_vbox)

    def on_login_connect_button_clicked(self, *args, **kwargs):
        """User wants to connect!"""
        if not self.login_ok_button.is_sensitive():
            return

        self._clear_warnings()

        error = False

        email = self.login_email_entry.get_text()
        msg = self._validate_email(email)
        if msg is not None:
            self.login_email_entry.set_warning(msg)
            error = True

        password = self.login_password_entry.get_text()
        if not password:
            self.login_password_entry.set_warning(FIELD_REQUIRED)
            error = True

        if error:
            return

        args = (self.app_name, email, password)
        if self.ping_url:
            f = self.backend.login_and_ping
            args = args + (self.ping_url,)
        else:
            f = self.backend.login

        error_handler = partial(self._handle_error, f, self.on_login_error)
        f(*args, reply_handler=NO_OP, error_handler=error_handler)

        self._set_current_page(self.processing_vbox)
        self.user_email = email
        self.user_password = password

    def on_login_back_button_clicked(self, *args, **kwargs):
        """User wants to go to the previous page."""
        self._set_current_page(self.enter_details_vbox)

    def on_forgotten_password_button_clicked(self, *args, **kwargs):
        """User wants to reset the password."""
        self._set_current_page(self.request_password_token_vbox)

    def on_request_password_token_ok_button_clicked(self, *args, **kwargs):
        """User entered the email address to reset the password."""
        if not self.request_password_token_ok_button.is_sensitive():
            return

        self._clear_warnings()

        email = self.reset_email_entry.get_text()
        msg = self._validate_email(email)
        if msg is not None:
            self.reset_email_entry.set_warning(msg)
            return

        logger.info('Calling request_password_reset_token with %r.', email)
        f = self.backend.request_password_reset_token
        error_handler = partial(self._handle_error, f,
                                self.on_password_reset_error)
        f(self.app_name, email,
          reply_handler=NO_OP, error_handler=error_handler)

        self._set_current_page(self.processing_vbox)

    def on_request_password_token_back_button_clicked(self, *args, **kwargs):
        """User wants to go to the previous page."""
        self._set_current_page(self.login_vbox)

    def on_reset_email_entry_changed(self, widget, *args, **kwargs):
        """User is changing the 'widget' entry in the reset email page."""
        sensitive = self._non_empty_input(widget)
        self.request_password_token_ok_button.set_sensitive(sensitive)

    def on_set_new_password_entries_changed(self, *args, **kwargs):
        """User is changing the 'widget' entry in the reset password page."""
        sensitive = True
        for entry in (self.reset_code_entry,
                      self.reset_password1_entry,
                      self.reset_password2_entry):
            sensitive &= self._non_empty_input(entry)
        self.set_new_password_ok_button.set_sensitive(sensitive)

    def on_set_new_password_ok_button_clicked(self, *args, **kwargs):
        """User entered reset code and new passwords."""
        if not self.set_new_password_ok_button.is_sensitive():
            return

        self._clear_warnings()

        error = False

        token = self.reset_code_entry.get_text()
        if not token:
            self.reset_code_entry.set_warning(FIELD_REQUIRED)
            error = True

        password1 = self.reset_password1_entry.get_text()
        password2 = self.reset_password2_entry.get_text()
        msg = self._validate_password(password1, password2)
        if msg is not None:
            self.reset_password1_entry.set_warning(msg)
            self.reset_password2_entry.set_warning(msg)
            error = True

        if error:
            return

        email = self.reset_email_entry.get_text()
        logger.info('Calling set_new_password with email %r, token %r and ' \
                    'new password: <hidden>.', email, token)
        f = self.backend.set_new_password
        error_handler = partial(self._handle_error, f,
                                self.on_password_change_error)
        f(self.app_name, email, token, password1,
          reply_handler=NO_OP, error_handler=error_handler)

        self._set_current_page(self.processing_vbox)

    def _webkit_init_ssl(self):
        """Set the WebKit ssl strictness."""
        # delay the import of webkit to be able to build without it
        from gi.repository import WebKit  # pylint: disable=E0611

        # Set the Soup session to be strict and use system CA certs
        session = WebKit.get_default_session()
        session.set_property(STRICT_SSL_PROP, True)
        session.set_property(CERTS_FILE_PROP, CA_CERT_FILE)

    def _add_webkit_browser(self):
        """Add the webkit browser for the t&c."""
        # delay the import of webkit to be able to build without it
        from gi.repository import WebKit  # pylint: disable=E0611

        self._webkit_init_ssl()

        browser = WebKit.WebView()

        browser.connect('notify::load-status',
                        self.on_tc_browser_notify_load_status)
        browser.connect('navigation-policy-decision-requested',
                        self.on_tc_browser_navigation_requested)

        settings = browser.get_settings()
        settings.set_property("enable-plugins", False)
        settings.set_property("enable-default-context-menu", False)

        # webkit_web_view_open has been deprecated since version 1.1.1 and
        # should not be used in newly-written code. Use
        # webkit_web_view_load_uri() instead.
        browser.load_uri(self.tc_url)
        browser.show()
        self.tc_browser_window.add(browser)

    def on_tc_button_clicked(self, *args, **kwargs):
        """The T&C button was clicked, create the browser and load terms."""
        if self.tc_browser_window.get_child() is None:
            self._add_webkit_browser()
            self._set_current_page(self.processing_vbox)
        else:
            self._set_current_page(self.tc_browser_vbox)

    def on_tc_back_button_clicked(self, *args, **kwargs):
        """T & C 'back' button was clicked, return to the previous page."""
        self._set_current_page(self.enter_details_vbox)

    def on_tc_browser_notify_load_status(self, browser, *args, **kwargs):
        """The T&C page is being loaded."""
        from gi.repository import WebKit  # pylint: disable=E0611

        if browser.get_load_status().real == WebKit.LoadStatus.FINISHED:
            self._set_current_page(self.tc_browser_vbox)

    def on_tc_browser_navigation_requested(self, browser, frame, request,
                                           action, decision, *args, **kwargs):
        """The user wants to navigate within the T&C browser."""
        from gi.repository import WebKit  # pylint: disable=E0611

        if action is not None and \
           action.get_reason() == WebKit.WebNavigationReason.LINK_CLICKED:
            if decision is not None:
                decision.ignore()
            url = action.get_original_uri()
            webbrowser.open(url)
        else:
            if decision is not None:
                decision.use()

    def on_tc_browser_vbox_hide(self, *args, **kwargs):
        """The T&C page is no longer being shown."""
        children = self.tc_browser_window.get_children()
        if len(children) > 0:
            browser = children[0]
            self.tc_browser_window.remove(browser)
            browser.destroy()
            del browser

    def on_captcha_reload_button_clicked(self, *args, **kwargs):
        """User clicked the reload captcha button."""
        self._generate_captcha()

    # backend callbacks

    def _build_general_error_message(self, errordict):
        """Concatenate __all__ and message from the errordict."""
        result = None
        msg1 = errordict.get('__all__')
        msg2 = errordict.get('message')
        if msg1 is not None and msg2 is not None:
            result = '\n'.join((msg1, msg2))
        else:
            result = msg1 if msg1 is not None else msg2
        return result

    @log_call
    def on_captcha_generated(self, app_name, captcha_id, *args, **kwargs):
        """Captcha image has been generated and is available to be shown."""
        if captcha_id is None:
            logger.warning('on_captcha_generated: captcha_id is None for '
                           'app_name %r.', app_name)
        self._captcha_id = captcha_id
        self._set_captcha_image()

    @log_call
    def on_captcha_generation_error(self, app_name, error, *args, **kwargs):
        """Captcha image generation failed."""
        self._set_warning_message(self.warning_label, CAPTCHA_LOAD_ERROR)
        self._generate_captcha()

    @log_call
    def on_user_registered(self, app_name, email, *args, **kwargs):
        """Registration can go on, user needs to verify email."""
        help_text = VERIFY_EMAIL_LABEL % {'app_name': self.app_name,
                                          'email': email}
        self.verify_email_vbox.help_text = help_text
        self._set_current_page(self.verify_email_vbox)

    @log_call
    def on_user_registration_error(self, app_name, error, *args, **kwargs):
        """Error in the data provided for registration."""
        msg = error.get('email')
        if msg is not None:
            self.email1_entry.set_warning(msg)
            self.email2_entry.set_warning(msg)

        msg = error.get('password')
        if msg is not None:
            self.password1_entry.set_warning(msg)
            self.password2_entry.set_warning(msg)

        msg = self._build_general_error_message(error)
        self._generate_captcha()
        self._set_current_page(self.enter_details_vbox, warning_text=msg)

    @log_call
    def on_email_validated(self, app_name, email, *args, **kwargs):
        """User email was successfully verified."""
        self.finish_success()

    @log_call
    def on_email_validation_error(self, app_name, error, *args, **kwargs):
        """User email validation failed."""
        msg = error.get('email_token')
        if msg is not None:
            self.email_token_entry.set_warning(msg)

        msg = self._build_general_error_message(error)
        self._set_current_page(self.verify_email_vbox, warning_text=msg)

    @log_call
    def on_logged_in(self, app_name, email, *args, **kwargs):
        """User was successfully logged in."""
        self.finish_success()

    @log_call
    def on_login_error(self, app_name, error, *args, **kwargs):
        """User was not successfully logged in."""
        msg = self._build_general_error_message(error)
        self._set_current_page(self.login_vbox, warning_text=msg)

    @log_call
    def on_user_not_validated(self, app_name, email, *args, **kwargs):
        """User was not validated."""
        self.on_user_registered(app_name, email)

    @log_call
    def on_password_reset_token_sent(self, app_name, email, *args, **kwargs):
        """Password reset token was successfully sent."""
        msg = SET_NEW_PASSWORD_LABEL % {'email': email}
        self.set_new_password_vbox.help_text = msg
        self._set_current_page(self.set_new_password_vbox)

    @log_call
    def on_password_reset_error(self, app_name, error, *args, **kwargs):
        """Password reset failed."""
        msg = self._build_general_error_message(error)
        self._set_current_page(self.login_vbox, warning_text=msg)

    @log_call
    def on_password_changed(self, app_name, email, *args, **kwargs):
        """Password was successfully changed."""
        self._set_current_page(self.login_vbox,
                               warning_text=PASSWORD_CHANGED)

    @log_call
    def on_password_change_error(self, app_name, error, *args, **kwargs):
        """Password reset failed."""
        msg = self._build_general_error_message(error)
        self._set_current_page(self.request_password_token_vbox,
                               warning_text=msg)
