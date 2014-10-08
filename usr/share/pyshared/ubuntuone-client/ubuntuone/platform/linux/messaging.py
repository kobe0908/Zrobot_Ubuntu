# ubuntuone.syncdaemon.platform.messaging - Messages to the user
#
# Author: Eric Casteleijn <eric.casteleijn@canonical.com>
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
"""Module that implements sending messages to the end user."""

# TODO: We may want to enable different messaging systems. When none
# of them are available, we should fall back to silently discarding
# messages.

import sys

indicate = None
glib = None
try:
    if 'gobject' in sys.modules and sys.modules['gobject'] is not None:
        import indicate as pyindicate
        import glib as GLib
        indicate = pyindicate
        glib = GLib
        using_gi = False
    else:
        from gi.repository import GLib
        glib = GLib
        from gi.repository import Indicate
        indicate = Indicate
        using_gi = True
except ImportError:
    pass

DBUS_BUS_NAME = 'com.ubuntuone.controlpanel.gui'
DBUS_PATH = '/gui'
DBUS_IFACE_GUI = 'com.ubuntuone.controlpanel.gui'
TRANSLATION_DOMAIN = 'ubuntuone-control-panel'

from ubuntuone.status.messaging import AbstractMessaging


def open_volumes():
    """Open the control panel to the shares tab."""
    _server_callback(None)


def _server_callback(the_indicator, message_time=None):
    """Open the control panel to the shares tab."""
    glib.spawn_command_line_async('ubuntuone-installer')
# pylint: enable=W0613


class Messaging(AbstractMessaging):
    """Notification of the end user."""

    def __init__(self, server_callback=_server_callback):
        self.server_callback = server_callback
        self.indicators = []
        if indicate is None:
            return
        if using_gi:
            self.server = indicate.Server.ref_default()
        else:
            self.server = indicate.indicate_server_ref_default()
        self.server.connect("server-display", server_callback)
        self.server.set_type("message.u1")
        self.server.set_desktop_file(
            "/usr/share/applications/ubuntuone-installer.desktop")
        self.server.show()

    # pylint: disable=R0913
    def show_message(self, sender, callback=None, message_time=None,
                     message_count=None, icon=None):
        """Show a message in the messaging menu."""
        if indicate is None:
            return
        indicator = indicate.Indicator()
        indicator.set_property("subtype", "u1")
        indicator.set_property("name", sender)
        indicator.set_property("sender", sender)

        if callback is None:
            callback = self.create_callback()
        indicator.connect("user-display", callback)

        if icon is not None:
            indicator.set_property_icon("icon", icon)
        if message_count is not None:
            indicator.set_property("count", str(message_count))
        else:
            if message_time is not None:
                indicator.set_property_time("time", message_time)
        indicator.set_property("draw-attention", "true")
        indicator.show()
        self.indicators.append(indicator)
    # pylint: enable=R0913

    def create_callback(self):
        """Create the callback to be used."""

        def callback(indicator, message_time=None):  # pylint: disable=W0613
            """Callback to be executed when message is clicked."""
            open_volumes()
            indicator.set_property("draw-attention", "false")
            indicator.hide()
            self.indicators.remove(indicator)
        return callback

    def update_count(self, indicator, add_count):
        """Update the count for an existing indicator."""
        new_count = int(indicator.get_property('count')) + add_count
        indicator.set_property('count', str(new_count))
