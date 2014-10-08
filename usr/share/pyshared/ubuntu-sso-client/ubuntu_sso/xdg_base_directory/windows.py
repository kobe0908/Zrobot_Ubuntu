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
"""XDG helpers for windows."""

import os
import sys


# pylint: disable=C0103
def get_special_folders():
    """ Routine to grab all the Windows Special Folders locations.

    If successful, returns dictionary
    of shell folder locations indexed on Windows keyword for each;
    otherwise, returns an empty dictionary.
    """
    # pylint: disable=W0621, F0401, E0611
    special_folders = {}

    from win32com.shell import shell, shellcon
    # CSIDL_LOCAL_APPDATA = C:\Users\<username>\AppData\Local
    # CSIDL_PROFILE = C:\Users\<username>
    # CSIDL_COMMON_APPDATA = C:\ProgramData
    # More information on these constants at
    # http://msdn.microsoft.com/en-us/library/bb762494

    # as per http://msdn.microsoft.com/en-us/library/windows/desktop/bb762181,
    # SHGetFolderPath is deprecated, we should migrate to SHGetKnownFolderPath
    # (http://msdn.microsoft.com/en-us/library/windows/desktop/bb762188)
    get_path = lambda name: shell.SHGetFolderPath(
        0, getattr(shellcon, name), None, 0).encode('utf8')
    special_folders['Personal'] = get_path("CSIDL_PROFILE")
    special_folders['Local AppData'] = get_path("CSIDL_LOCAL_APPDATA")
    special_folders['AppData'] = os.path.dirname(
        special_folders['Local AppData'])
    special_folders['Common AppData'] = get_path("CSIDL_COMMON_APPDATA")
    return special_folders


def get_env_path(key, default):
    """Get a utf8 path from an environment variable."""
    if key in os.environ:
        # on windows, environment variables are mbcs bytes
        # so we must turn them into utf-8 Syncdaemon paths
        path = os.environ.get(key)
        return path.decode(sys.getfilesystemencoding()).encode("utf-8")
    else:
        return default


special_folders = get_special_folders()

home_path = special_folders['Personal']
app_local_data_path = special_folders['Local AppData']
app_global_data_path = special_folders['Common AppData']

xdg_data_home = get_env_path('XDG_DATA_HOME',
    os.path.join(app_local_data_path, 'xdg'))

xdg_cache_home = get_env_path('XDG_CACHE_HOME',
    os.path.join(xdg_data_home, 'cache'))

xdg_config_home = get_env_path('XDG_CONFIG_HOME',
    app_local_data_path)


def get_data_dirs():
    """Returns XDG data directories."""
    return get_env_path('XDG_DATA_DIRS',
        '{0}{1}{2}'.format(app_local_data_path, os.pathsep,
        app_global_data_path)).split(os.pathsep)


xdg_data_dirs = get_data_dirs()


def get_config_dirs():
    """Return XDG config directories."""
    return [xdg_config_home] + \
        get_env_path('XDG_CONFIG_DIRS',
            app_global_data_path,
            ).split(os.pathsep)

xdg_config_dirs = get_config_dirs()

xdg_data_dirs = filter(lambda x: x, xdg_data_dirs)
xdg_config_dirs = filter(lambda x: x, xdg_config_dirs)
