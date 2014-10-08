# -*- encoding: utf-8 -*-
#
# Copyright 2009-2012 Canonical Ltd.
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
"""Platform specific bindings."""

import os
import sys

from ubuntu_sso.xdg_base_directory import xdg_home

# very hackish way to avoid "import *" to satisfy pyflakes
# and to avoid import ubuntuone.platform.X as source (it wont work)

if sys.platform == "win32":
    from ubuntuone.platform import windows
    source = windows
else:
    from ubuntuone.platform import linux
    source = linux

# This imports needs to be here in order to belongs to this namespace
from ubuntuone.platform import credentials
from ubuntuone.platform import tools


def expand_user(path):
    """Fix Python expanduser for weird chars in windows."""
    assert isinstance(path, str)
    try:
        path.decode('utf-8')
    except UnicodeDecodeError:
        raise AssertionError('The path %r must be encoded in utf-8' % path)
    tilde = '~'
    if not path.startswith(tilde) or \
    (len(path) > 1 and path[1:2] != os.path.sep):
        return path
    result = path.replace('~', xdg_home, 1)

    assert isinstance(result, str)
    try:
        result.decode('utf-8')
    except UnicodeDecodeError:
        raise AssertionError('The path %r must be encoded in utf-8' % result)
    return result


platform = source.platform
access = source.access
allow_writes = source.allow_writes
can_write = source.can_write
get_path_list = source.get_path_list
is_link = source.is_link
is_root = source.is_root
listdir = source.listdir
make_dir = source.make_dir
make_link = source.make_link
move_to_trash = source.move_to_trash
native_rename = source.native_rename
normpath = source.normpath
open_file = source.open_file
path_exists = source.path_exists
read_link = source.read_link
recursive_move = source.recursive_move
remove_dir = source.remove_dir
remove_file = source.remove_file
remove_link = source.remove_link
remove_tree = source.remove_tree
rename = source.rename
set_application_name = source.set_application_name
set_dir_readonly = source.set_dir_readonly
set_dir_readwrite = source.set_dir_readwrite
set_file_readonly = source.set_file_readonly
set_file_readwrite = source.set_file_readwrite
set_no_rights = source.set_no_rights
stat_path = source.stat_path
walk = source.walk

# From Logger
setup_filesystem_logging = source.setup_filesystem_logging
get_filesystem_logger = source.get_filesystem_logger

# From File System Notifications
FilesystemMonitor = source.FilesystemMonitor
_GeneralINotifyProcessor = source._GeneralINotifyProcessor

# IPC
ExternalInterface = source.ExternalInterface
is_already_running = source.is_already_running
