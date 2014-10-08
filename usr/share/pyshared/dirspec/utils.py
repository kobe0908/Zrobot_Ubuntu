# -*- coding: utf-8 -*-
#
# Copyright 2011 Canonical Ltd.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License version 3
# as published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""Utilities for multiplatform support of XDG directory handling."""

import os
import sys

__all__ = ['user_home',
           'default_cache_home',
           'default_config_home',
           'default_config_path',
           'default_data_home',
           'default_data_path',
           'get_env_path',
           'unicode_path',
           ]


def get_env_path(key, default):
    """Get a UTF-8 encoded path from an environment variable."""
    if key in os.environ:
        # on windows, environment variables are mbcs bytes
        # so we must turn them into utf-8 Syncdaemon paths
        path = os.environ.get(key)
        return path.decode(sys.getfilesystemencoding()).encode("utf-8")
    else:
        return default


def unicode_path(utf8path):
    """Turn an utf8 path into a unicode path."""
    return utf8path.decode("utf-8")


def get_special_folders():
    """ Routine to grab all the Windows Special Folders locations.

    If successful, returns dictionary
    of shell folder locations indexed on Windows keyword for each;
    otherwise, returns an empty dictionary.
    """
    # pylint: disable=W0621, F0401, E0611
    special_folders = {}

    if sys.platform == 'win32':
        from win32com.shell import shell, shellcon
        # CSIDL_LOCAL_APPDATA = C:\Users\<username>\AppData\Local
        # CSIDL_PROFILE = C:\Users\<username>
        # CSIDL_COMMON_APPDATA = C:\ProgramData
        # More information on these constants at
        # http://msdn.microsoft.com/en-us/library/bb762494

        # per http://msdn.microsoft.com/en-us/library/windows/desktop/bb762181,
        # SHGetFolderPath is deprecated, replaced by SHGetKnownFolderPath
        # (http://msdn.microsoft.com/en-us/library/windows/desktop/bb762188)
        get_path = lambda name: shell.SHGetFolderPath(
            0, getattr(shellcon, name), None, 0).encode('utf8')
        special_folders['Personal'] = get_path("CSIDL_PROFILE")
        special_folders['Local AppData'] = get_path("CSIDL_LOCAL_APPDATA")
        special_folders['AppData'] = os.path.dirname(
            special_folders['Local AppData'])
        special_folders['Common AppData'] = get_path("CSIDL_COMMON_APPDATA")

    return special_folders


# pylint: disable=C0103
if sys.platform == 'win32':
    special_folders = get_special_folders()
    user_home = special_folders['Personal']
    default_config_path = special_folders['Common AppData']
    default_config_home = special_folders['Local AppData']
    default_data_path = os.path.join(default_config_path, 'xdg')
    default_data_home = os.path.join(default_config_home, 'xdg')
    default_cache_home = os.path.join(default_data_home, 'cache')
else:
    user_home = os.path.expanduser('~')
    default_cache_home = os.path.join(user_home, '.cache')
    default_config_path = '/etc/xdg'
    default_config_home = os.path.join(user_home, '.config')
    default_data_path = '/usr/local/share:/usr/share'
    default_data_home = os.path.join(user_home, '.local', 'share')
