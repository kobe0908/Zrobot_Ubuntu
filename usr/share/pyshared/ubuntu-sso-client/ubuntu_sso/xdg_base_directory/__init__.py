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
"""XDG multiplatform."""

import os
import sys
import warnings


def unicode_path(utf8path):
    """Turn an utf8 path into a unicode path."""
    return utf8path.decode("utf-8")


def native_path(utf8path):
    """Turn an utf8 path into a path useable in the current encoding."""
    warnings.warn('native_path will be removed soon', DeprecationWarning)
    return unicode_path(utf8path)


def syncdaemon_path(mbcspath):
    """Turn a mbcs path in a utf-8 path as CURRENTLY used inside syncdaemon."""
    warnings.warn('syncdaemon_path will be removed soon', DeprecationWarning)
    return mbcspath.decode(sys.getfilesystemencoding()).encode("utf-8")


# pylint: disable=C0103,F0401,E0611,E1101
if sys.platform == "win32":
    from ubuntu_sso.xdg_base_directory import windows
    source = windows
    xdg_home = source.home_path
else:
    import xdg.BaseDirectory
    source = xdg.BaseDirectory
    xdg_home = os.path.expanduser('~')

xdg_cache_home = source.xdg_cache_home

xdg_config_home = source.xdg_config_home
xdg_config_dirs = source.xdg_config_dirs

xdg_data_home = source.xdg_data_home
xdg_data_dirs = source.xdg_data_dirs


def load_config_paths(*resource):
    """Iterator of configuration paths.

    Return an iterator which gives each directory named 'resource' in
    the configuration search path. Information provided by earlier
    directories should take precedence over later ones (ie, the user's
    config dir comes first).
    """
    resource = os.path.join(*resource)
    for config_dir in xdg_config_dirs:
        path = os.path.join(config_dir, resource)
        # access the file system always with unicode
        # to properly behave in some operating systems
        if os.path.exists(unicode_path(path)):
            yield path


def save_config_path(*resource):
    """Path to save configuration.

    Ensure $XDG_CONFIG_HOME/<resource>/ exists, and return its path.
    'resource' should normally be the name of your application. Use this
    when SAVING configuration settings. Use the xdg_config_dirs variable
    for loading.
    """
    resource = os.path.join(*resource)
    assert not resource.startswith('/')
    path = os.path.join(xdg_config_home, resource)
    # access the file system always with unicode
    # to properly behave in some operating systems
    if not os.path.isdir(unicode_path(path)):
        os.makedirs(unicode_path(path), 0700)
    return path
