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

import gettext
import os
import urlparse

# pylint: disable=E0611,F0401
from gi.repository import Gio, GObject, Gtk, RB
from gi.repository.UbuntuOneUI import MusicStore as U1MusicStore
# pylint: enable=E0611,F0401

from gettext import lgettext as _

gettext.bindtextdomain("rhythmbox-ubuntuone", "/usr/share/locale")
gettext.textdomain("rhythmbox-ubuntuone")

MUSIC_STORE_WIDGET = U1MusicStore()
U1LIBRARYPATH = MUSIC_STORE_WIDGET.get_library_location()


class U1EntryType(RB.RhythmDBEntryType):
    """Entry type for the Ubuntu One Music Store source."""

    def __init__(self):
        RB.RhythmDBEntryType.__init__(self, name='ubuntuone')

    def do_can_sync_metadata(self, entry):
        """Not a real source, so we can't sync metadata."""
        return False

    def do_sync_metadata(self, entry, changes):
        """Do nothing."""
        return


class U1MusicStoreWidget(object):
    """The Ubuntu One Music Store."""
    def __init__(self, plugin):
        self.plugin = plugin
        self.db = None
        self.shell = None
        self.source = None
        self.entry_type = U1EntryType()

    def activate(self, shell):
        """Plugin startup."""
        self.db = shell.get_property("db")
        group = RB.DisplayPageGroup.get_by_id("stores")

        icon = Gtk.IconTheme.get_default().load_icon(
            "ubuntuone", 24, 0)

        self.db.register_entry_type(self.entry_type)

        self.source = GObject.new(U1Source,
                                  shell=shell,
                                  entry_type=self.entry_type,
                                  pixbuf=icon,
                                  plugin=self.plugin)
        shell.register_entry_type_for_source(self.source, self.entry_type)
        shell.append_display_page(self.source, group)

        self.shell = shell
        self.source.connect("preview-mp3", self.play_preview_mp3)
        self.source.connect("play-library", self.play_library)
        self.source.connect("download-finished", self.download_finished)
        self.source.connect("url-loaded", self.url_loaded)

        self.source.props.query_model = RB.RhythmDBQueryModel.new_empty(
            self.db)

    def deactivate(self, shell):
        """Plugin shutdown."""
        # remove source
        self.source.delete_thyself()
        # delete held references
        del self.db
        del self.source
        del self.shell

    def url_loaded(self, source, url):
        """A URL is loaded in the plugin"""
        if urlparse.urlparse(url)[2] == "https":
            pass
        else:
            pass

    def _udf_path_to_library_uri(self, path):
        """Build a URI from the path for the song in the library."""
        if path.startswith(U1LIBRARYPATH):
            library_path = path
        else:
            subpath = path
            if subpath.startswith("/"):
                subpath = subpath[1:]
            library_path = os.path.join(U1LIBRARYPATH, subpath)
        # convert path to URI. Don't use urllib for this; Python and
        # glib escape URLs differently. gio does it the glib way.
        return Gio.File.new_for_path(library_path).get_uri()

    def download_finished(self, source, path):
        """A file is finished downloading"""
        library_uri = self._udf_path_to_library_uri(path)
        # Import the URI
        if not self.db.entry_lookup_by_location(library_uri):
            self.db.add_uri(library_uri)

    def play_library(self, source, path):
        """Switch to and start playing a song from the library"""
        uri = self._udf_path_to_library_uri(path)
        entry = self.db.entry_lookup_by_location(uri)
        if not entry:
            print "couldn't find entry", uri
            return
        libsrc = self.shell.props.library_source
        artist_view, album_view = libsrc.get_property_views()[0:2]
        song_view = libsrc.get_entry_view()
        artist = entry.get_string(RB.RhythmDBPropType.ARTIST)
        album = entry.get_string(RB.RhythmDBPropType.ALBUM)
        self.shell.props.display_page_tree.select(libsrc)
        artist_view.set_selection([artist])
        album_view.set_selection([album])
        song_view.scroll_to_entry(entry)
        player = self.shell.get_property('shell-player')
        player.stop()
        player.play_entry(entry, libsrc)

    def play_preview_mp3(self, source, url, title):
        """Play a passed mp3; signal handler for preview-mp3 signal."""
        # create an entry, don't save it, and play it
        entry = RB.RhythmDBEntry.new(self.db, self.entry_type, url)
        self.db.entry_set(entry, RB.RhythmDBPropType.TITLE, title)
        player = self.shell.get_property('shell-player')
        player.stop()
        player.play_entry(entry, self.source)


class U1Source(RB.Source):
    """A Rhythmbox source widget for the U1 Music Store."""
    # gproperties required so that rb.Source is instantiable
    __gproperties__ = {
      'plugin': (GObject.GObject, 'plugin', 'plugin',
                 GObject.PARAM_WRITABLE | GObject.PARAM_CONSTRUCT_ONLY),
      }
    # we have the preview-mp3 signal; we receive it from the widget, and
    # re-emit it so that the plugin gets it, because the plugin actually
    # plays the mp3
    __gsignals__ = {
      "preview-mp3": (GObject.SIGNAL_RUN_FIRST,
                      GObject.TYPE_NONE, (str, str)),
      "play-library": (GObject.SIGNAL_RUN_FIRST,
                       GObject.TYPE_NONE, (str,)),
      "download-finished": (GObject.SIGNAL_RUN_FIRST,
                            GObject.TYPE_NONE, (str,)),
      "url-loaded": (GObject.SIGNAL_RUN_FIRST,
                     GObject.TYPE_NONE, (str,)),
    }

    def __init__(self):
        RB.Source.__init__(self, name=_("Ubuntu One"))
        self.browser = MUSIC_STORE_WIDGET
        self.__activated = False
        self.__plugin = None
        self.add_music_store_widget()

    def do_impl_activate(self):
        """Source startup."""
        if self.__activated:
            return
        self.__activated = True
        RB.Source.do_impl_activate(self)

    def do_impl_want_uri(self, uri):
        """I want to handle u1ms URLs"""
        if uri.startswith("u1ms://"):
            return 100
        return 0

    def do_impl_add_uri(self, uri, title, genre, callback=None,
                        callback_data=None, destroy_data=None):
        """Handle a u1ms URL"""
        if not uri.startswith("u1ms://"):
            return
        uri_to_use = uri.replace("u1ms://", "http://")
        # pylint: disable=E1101
        shell = self.get_property("shell")
        shell.props.display_page_tree.select(self)
        self.browser.load_store_link(uri_to_use)
        if callback is not None:
            callback(callback_data)
            if destroy_data is not None:
                destroy_data(callback_data)

    def add_music_store_widget(self):
        """Display the music store widget in Rhythmbox."""
        # pylint: disable=E1101
        if self.browser.get_property('parent') is None:
            self.add(self.browser)
        else:
            self.browser.reparent(self)
        self.browser.show()
        self.show()
        self.browser.set_property("visible", True)
        self.browser.connect("preview-mp3",
                             self.re_emit_preview)
        self.browser.connect("play-library",
                             self.re_emit_playlibrary)
        self.browser.connect("download-finished",
                             self.re_emit_downloadfinished)
        self.browser.connect("url-loaded",
                             self.re_emit_urlloaded)

    def do_impl_can_pause(self):
        """Implementation can pause.
           If we don't handle this, Rhythmbox segfaults."""
        return True  # so we can pause, else we segfault

    def re_emit_preview(self, widget, url, title):
        """Handle the preview-mp3 signal and re-emit it."""
        # pylint: disable=E1101
        self.emit("preview-mp3", url, title)

    def re_emit_playlibrary(self, widget, path):
        """Handle the play-library signal and re-emit it."""
        # pylint: disable=E1101
        self.emit("play-library", path)

    def re_emit_downloadfinished(self, widget, path):
        """Handle the download-finished signal and re-emit it."""
        # pylint: disable=E1101
        self.emit("download-finished", path)

    def re_emit_urlloaded(self, widget, url):
        """Handle the url-loaded signal and re-emit it."""
        # pylint: disable=E1101
        self.emit("url-loaded", url)

    def do_set_property(self, prop, value):
        """Allow property settings to handle the plug-in call."""
        if prop.name == 'plugin':
            self.__plugin = value
        else:
            raise AttributeError('unknown property %s' % prop.name)
