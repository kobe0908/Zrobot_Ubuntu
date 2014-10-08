# -*- coding: utf-8 -*-
#
# Copyright 2011-2012 Canonical Ltd.
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
"""The GUI of the Ubuntu One Installer."""

import aptdaemon.gtk3widgets as aptgtk
import aptdaemon.client as aptclient
import gettext
import os

from aptdaemon.enums import EXIT_SUCCESS
from gi.repository import Gtk, GObject, GLib, Gdk, GdkPixbuf, Pango
from ubuntuone.installer import (CLIENT_SHELL_PACKAGE,
                                 CONTROL_PANEL_COMMAND,
                                 CONTROL_PANEL_PACKAGE,
                                 MUSIC_STORE_PACKAGE,
                                 is_installed)

# Some shenanigans to deal with pyflakes complaining
inline_callbacks = None
try:
    from defer import inline_callbacks
except ImportError:
    from aptdaemon.defer import inline_callbacks as old_callbacks

if inline_callbacks is None:
    inline_callbacks = old_callbacks

gettext.install(domain='ubuntuone-installer', unicode=True)
if '_' not in __builtins__:
    _ = gettext.gettext


class UnsupportedDistribution(BaseException):
    """Exception for when on an unsupported distribution."""


class VSeparator(Gtk.VSeparator):
    """A dotted line separator."""

    def do_draw(self, cairo_context):
        """Draw some magic."""
        sc = self.get_style_context()
        state = self.get_state_flags()
        width = self.get_allocated_width()
        height = self.get_allocated_height()

        sc.save()
        sc.set_state(state)

        y = 0
        x = width / 2
        while y < height:
            Gtk.render_activity(sc, cairo_context, float(x), float(y), 1, 1)
            y += 3

        sc.restore()
        return True


class HSeparator(Gtk.HSeparator):
    """A dotted line separator."""

    def do_draw(self, cairo_context):
        """Draw some magic."""
        sc = self.get_style_context()
        state = self.get_state_flags()
        width = self.get_allocated_width()
        height = self.get_allocated_height()

        sc.save()
        sc.set_state(state)

        x = 0
        y = height / 2
        while x <= width:
            Gtk.render_activity(sc, cairo_context,
                                float(x), float(y), 1.0, 1.0)
            x += 3

        sc.restore()
        return True


class Window(Gtk.Window):
    """The main dialog to use."""

    __gsignals__ = {'response': (GObject.SIGNAL_RUN_LAST,
                                 GObject.TYPE_NONE,
                                 (GObject.TYPE_INT,)),
                    }

    def __init__(self):
        Gtk.Window.__init__(self)
        self.set_title('Ubuntu One')
        self.set_default_icon_name('ubuntuone-installer')
        self.set_type_hint(Gdk.WindowTypeHint.DIALOG)
        self.set_position(Gtk.WindowPosition.CENTER)

        vbox = Gtk.VBox()
        vbox.set_border_width(12)
        vbox.set_spacing(24)
        self.add(vbox)
        vbox.show()

        self.__header = Gtk.HBox()
        self.__header.set_spacing(64)
        vbox.pack_start(self.__header, False, False, 0)
        self.__header.show()

        self.__hlabelbox = Gtk.VBox()
        self.__hlabelbox.set_spacing(12)
        self.__header.pack_start(self.__hlabelbox, True, True, 0)
        self.__hlabelbox.show()

        self.__hlabel = Gtk.Label((u'<span size="xx-large">{}</span>').format(
                _(u'Install Ubuntu One')))
        self.__hlabel.set_use_markup(True)
        self.__hlabel.set_alignment(0.0, 0.0)
        self.__hlabelbox.pack_start(self.__hlabel, False, False, 0)
        self.__hlabel.show()

        self.__hlabel2 = Gtk.Label((u'<span size="large">{}</span>').format(
                _(u'Discover your personal cloud')))
        self.__hlabel2.set_use_markup(True)
        self.__hlabel2.set_alignment(0.0, 0.0)
        self.__hlabelbox.pack_start(self.__hlabel2, False, False, 0)
        self.__hlabel2.show()

        self.__hlogo = Gtk.Image()
        self.__header.pack_end(self.__hlogo, False, False, 0)
        self.__hlogo.show()

        logo = self.__find_data_file('u1logo.svg')
        if logo:
            self.__hlogo.set_from_file(logo)

        self.__notebook = Gtk.Notebook()
        self.__notebook.set_show_tabs(False)
        self.__notebook.set_show_border(False)
        self.__notebook.set_scrollable(False)
        self.__notebook.popup_disable()

        self.__info_page = self.__construct_info_page()
        self.__notebook.append_page(self.__info_page, None)
        self.__info_page.show()

        # Our progressbar widget
        self.__apt_progress = aptgtk.AptProgressBar()

        self.__progress_page = self.__construct_progress_page()
        self.__notebook.append_page(self.__progress_page, None)
        self.__progress_page.show()

        # Label widget for error text
        self.__err_label = Gtk.Label('')
        self.__err_label.set_ellipsize(Pango.EllipsizeMode.MIDDLE)
        self.__err_label.set_line_wrap(True)

        self.__error_page = self.__construct_error_page()
        self.__notebook.append_page(self.__error_page, None)
        self.__error_page.show()

        vbox.pack_start(self.__notebook, False, False, 0)
        self.__notebook.show()

        self.__action_area = Gtk.HButtonBox()
        self.__action_area.set_spacing(12)
        self.__action_area.set_layout(Gtk.ButtonBoxStyle.END)
        vbox.pack_end(self.__action_area, False, True, 0)
        self.__action_area.show()

        self.__cancel_button = Gtk.Button.new_from_stock(Gtk.STOCK_CANCEL)
        self.__cancel_button.connect('clicked', lambda x: self.emit(
                'response', Gtk.ResponseType.CANCEL))
        self.__action_area.add(self.__cancel_button)
        self.__cancel_button.show()

        self.__main_button = Gtk.Button.new_with_mnemonic(_(u'I_nstall'))
        self.__main_button.set_image(Gtk.Image.new_from_stock(
                Gtk.STOCK_EXECUTE, Gtk.IconSize.BUTTON))
        self.__main_button.connect('clicked', lambda x: self.emit(
                'response', Gtk.ResponseType.OK))
        self.__action_area.add(self.__main_button)
        self.__main_button.grab_focus()
        self.__main_button.show()

        # Button for error conditions
        self.__close_button = Gtk.Button.new_from_stock(Gtk.STOCK_CLOSE)
        self.__close_button.connect('clicked', lambda x: self.emit(
                'response', Gtk.ResponseType.CANCEL))
        self.__action_area.add(self.__close_button)

        # Button for the external link
        self.__lm_button = Gtk.LinkButton.new_with_label(
            'https://one.ubuntu.com/', _(u'Learn more'))
        self.__action_area.add(self.__lm_button)
        self.__action_area.set_child_secondary(self.__lm_button, True)
        self.__lm_button.show()

        self.connect('destroy', self.destroyed)
        self.connect('response', self.__got_response)
        self.connect('delete-event', lambda x, y: self.emit(
                        'response', Gtk.ResponseType.DELETE_EVENT))

        self.client = aptclient.AptClient()

    def __find_data_file(self, filename):
        """Find the full path for the specified data file."""
        path = os.path.join(os.getcwd(), 'data', filename)
        if os.path.exists(path):
            return path

        path = os.path.join(os.getcwd(), os.path.pardir, 'data', filename)
        if os.path.exists(path):
            return os.path.abspath(path)

        path = os.path.join(os.getcwd(), os.path.pardir, os.path.pardir,
                            'data', filename)
        if os.path.exists(path):
            return os.path.abspath(path)

        for folder in GLib.get_system_data_dirs():
            path = os.path.join(folder, 'ubuntuone-installer', filename)
            if os.path.exists(path):
                return path

    def __get_package_list(self):
        """Build the list of packages, to only include non-installed ones."""
        packages = []
        if not is_installed(CONTROL_PANEL_PACKAGE, CONTROL_PANEL_COMMAND):
            packages.append(CONTROL_PANEL_PACKAGE)
        if not is_installed(MUSIC_STORE_PACKAGE):
            packages.append(MUSIC_STORE_PACKAGE)
        if not is_installed(CLIENT_SHELL_PACKAGE):
            packages.append(CLIENT_SHELL_PACKAGE)

        return packages

    def __got_response(self, dialog, response):
        """Handle the dialog response actions."""
        if response in [Gtk.ResponseType.CANCEL,
                        Gtk.ResponseType.DELETE_EVENT]:
            self.destroy()
            Gtk.main_quit()
            return
        elif response == Gtk.ResponseType.OK:
            self.__do_install()

    def __construct_info_page(self):
        """Build the initial info page."""
        page = Gtk.HBox()
        page.set_spacing(12)
        page.show()

        # Get the width of a larger character in pixels
        layout = page.create_pango_layout(u'W')
        (width, height) = layout.get_size()
        width = width / Pango.SCALE
        height = height / Pango.SCALE

        table = Gtk.Table(5, 2, False)
        table.set_row_spacings(6)
        table.set_col_spacings(12)
        page.pack_start(table, True, True, 0)
        table.show()

        image = Gtk.Image()
        table.attach_defaults(image, 0, 1, 0, 5)
        image.show()
        path = self.__find_data_file('u1cloud.svg')
        if path:
            pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(
                path, 320, 240, True)
            image.set_from_pixbuf(pixbuf)

        # Get the width in chars based on cloud width, for main labels
        width_chars = (image.get_pixbuf().get_width() / width) * 2.0

        label = Gtk.Label(_(u'Store files, photos, and music safely in Ubuntu'
                            ' One and access them on any of your devices.'))
        label.set_max_width_chars(width_chars)
        label.set_width_chars(width_chars)
        label.set_use_markup(True)
        label.set_line_wrap(True)
        label.set_alignment(0.0, 0.5)
        label.set_justify(Gtk.Justification.LEFT)
        table.attach_defaults(label, 1, 2, 0, 1)
        label.show()

        separator = HSeparator()
        table.attach_defaults(separator, 1, 2, 1, 2)
        separator.show()

        label = Gtk.Label(_(u'Upload photos from your mobile instantly, and'
                            ' they\'re ready to share with friends or post'
                            ' online.'))
        label.set_max_width_chars(width_chars)
        label.set_width_chars(width_chars)
        label.set_use_markup(True)
        label.set_line_wrap(True)
        label.set_alignment(0.0, 0.5)
        label.set_justify(Gtk.Justification.LEFT)
        table.attach_defaults(label, 1, 2, 2, 3)
        label.show()

        separator = HSeparator()
        table.attach_defaults(separator, 1, 2, 3, 4)
        separator.show()

        label = Gtk.Label(_(u'Stream your music collection to all of your'
                            ' devices and listen to any song - online or'
                            ' offline.'))
        label.set_max_width_chars(width_chars)
        label.set_width_chars(width_chars)
        label.set_use_markup(True)
        label.set_line_wrap(True)
        label.set_alignment(0.0, 0.5)
        label.set_justify(Gtk.Justification.LEFT)
        table.attach_defaults(label, 1, 2, 4, 5)
        label.show()

        return page

    def __construct_progress_page(self):
        """Build the install progress page."""
        page = Gtk.VBox()
        page.set_spacing(6)
        page.show()

        label = Gtk.Label(_(u'Ubuntu One is installing…'))
        label.set_alignment(0.0, 0.0)
        page.pack_start(label, False, True, 0)
        label.show()

        page.pack_start(self.__apt_progress, False, True, 0)
        self.__apt_progress.show()

        return page

    def __construct_error_page(self):
        """A page for showing errors to the user."""
        page = Gtk.HBox()
        page.set_spacing(12)
        page.show()

        image = Gtk.Image.new_from_stock(Gtk.STOCK_DIALOG_ERROR,
                                         Gtk.IconSize.DIALOG)
        image.set_alignment(0.5, 0.0)
        page.pack_start(image, False, False, 0)
        image.show()

        # Align and pack the error label
        self.__err_label.set_alignment(0.0, 0.0)
        page.pack_start(self.__err_label, True, True, 0)
        self.__err_label.show()

        return page

    def __got_error(self, error):
        """Got an error trying to set up Ubuntu One."""
        self.__cancel_button.hide()
        self.__main_button.show()
        self.__close_button.show()
        self.__err_label.set_text(error)
        self.__notebook.set_current_page(2)

    @inline_callbacks
    def __install_u1(self, *args, **kwargs):
        """Install the packages."""
        self.__apt_progress.set_fraction(0.0)

        def finished(transaction, exit_status, *args, **kwargs):
            if exit_status != EXIT_SUCCESS:
                self.__got_error(transaction.error_details)
            else:
                GLib.spawn_command_line_async(CONTROL_PANEL_COMMAND)
                Gtk.main_quit()

        transaction = yield self.client.install_packages(
            package_names=self.__get_package_list())
        transaction.connect('finished', finished)
        self.__apt_progress.set_transaction(transaction)
        transaction.run()

    @inline_callbacks
    def __update_cache(self, *args, **kwargs):
        """Update the cache."""
        self.__apt_progress.set_fraction(0.0)

        def finished(transaction, exit_status, *args, **kwargs):
            if exit_status != EXIT_SUCCESS:
                self.__got_error(transaction.error_details)
            else:
                self.__install_u1()

        transaction = yield self.client.update_cache(
            sources_list='/etc/apt/sources.list')
        transaction.connect('finished', finished)
        self.__apt_progress.set_transaction(transaction)
        transaction.run()

    def __do_install(self):
        """Do the install."""
        # Hide the buttons
        self.__cancel_button.hide()
        self.__main_button.hide()
        self.__close_button.hide()

        # Switch to the progress page
        self.__notebook.set_current_page(1)

        self.__update_cache()

    @property
    def active_page(self):
        """Get the active page."""
        return self.__notebook.get_current_page()

    def response(self, response):
        """Emit the response signal with the value response."""
        self.emit('response', int(response))

    def run(self):
        """Show the dialog and do what's necessary."""
        self.show()
