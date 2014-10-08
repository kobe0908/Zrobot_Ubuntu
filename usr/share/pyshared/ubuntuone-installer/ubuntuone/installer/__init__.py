# -*- coding: utf-8 -*-
#
# Copyright 2012 Canonical Ltd.
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
"""Ubuntu One Installer package."""

import apt

from gi.repository import GLib

CLIENT_SHELL_PACKAGE = 'ubuntuone-client-gnome'

CONTROL_PANEL_COMMAND = 'ubuntuone-control-panel-qt'
CONTROL_PANEL_PACKAGE = 'ubuntuone-control-panel-qt'

MUSIC_STORE_PACKAGE = 'rhythmbox-ubuntuone'


def is_installed(package, command='false'):
    """Check if things are installed already."""
    try:
        cache = apt.Cache()
        return package in cache and cache[package].is_installed
    except SystemError:
        return GLib.find_program_in_path(command) is not None
