# Copyright (C) 2009-2012 Canonical, Ltd.
#
# This library is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License
# version 3.0 as published by the Free Software Foundation.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License version 3.0 for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library. If not, see
# <http://www.gnu.org/licenses/>.
"""The Ubuntu One Rhythmbox plugin."""

# pylint: disable=E0611
from gi.repository import Gio, GObject, Peas
# pylint: enable=E0611

# pylint: disable=W0403
from MusicStoreWidget import U1MusicStoreWidget, U1LIBRARYPATH
# pylint: enable=W0403


class UbuntuOnePlugin (GObject.GObject, Peas.Activatable):
    """Ubuntu One integration for Rhythmbox."""
    __gtype_name__ = 'UbuntuOnePlugin'
    object = GObject.property(type=GObject.GObject)

    def __init__(self):
        GObject.GObject.__init__(self)

        # RhythmDB settings so we can handle changes
        self.rdbconf = Gio.Settings('org.gnome.rhythmbox.rhythmdb')
        self.rdbconf.connect('changed::locations', self._locations_changed)

        # The Music Store itself
        self.music_store_widget = U1MusicStoreWidget(plugin=self)

    def _locations_changed(self, *args, **kwargs):
        """Handle the locations setting being changed."""
        libraries = self.rdbconf.get_strv('locations')
        library_uri = Gio.File.new_for_path(U1LIBRARYPATH).get_uri()
        if library_uri not in libraries:
            libraries.append(library_uri)
            self.rdbconf.set_strv('locations', libraries)
        # Remove the non-uri path if it exists
        if U1LIBRARYPATH in libraries:
            libraries.remove(U1LIBRARYPATH)
            self.rdbconf.set_strv('locations', libraries)
        # Remove the unescaped uri path if it exists
        unescaped_path = u'file://{0}'.format(U1LIBRARYPATH)
        if unescaped_path in libraries:
            libraries.remove(unescaped_path)
            self.rdbconf.set_strv('locations', libraries)

    def do_activate(self):
        """Plug-in startup."""
        # Add the Ubuntu One purchased music directory if not already added
        self._locations_changed()
        self.music_store_widget.activate(self.object)

    def do_deactivate(self):
        """Plug-in shutdown."""
        self.music_store_widget.deactivate(self.object)
