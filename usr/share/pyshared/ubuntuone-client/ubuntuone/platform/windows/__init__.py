# ubuntuone.platform.windows - windows platform imports
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
"""
Windows import for ubuntuone-client

This module has to have all windows specific modules and provide the api
required to support the windows platform.
"""

platform = "win32"


import constants
import event_logging
import filesystem_notifications
import launcher
import logger
import messaging
import notification
import os_helper
import session

from ubuntuone.platform.windows.os_helper import (
    access,
    allow_writes,
    can_write,
    get_path_list,
    is_link,
    is_root,
    listdir,
    make_dir,
    make_link,
    move_to_trash,
    native_rename,
    normpath,
    open_file,
    path_exists,
    read_link,
    recursive_move,
    remove_dir,
    remove_file,
    remove_link,
    remove_tree,
    rename,
    set_application_name,
    set_dir_readonly,
    set_dir_readwrite,
    set_file_readonly,
    set_file_readwrite,
    set_no_rights,
    stat_path,
    walk,
)
from ubuntuone.platform.windows import event_logging
from ubuntuone.platform.windows.logger import (
    setup_filesystem_logging,
    get_filesystem_logger,
)
from ubuntuone.platform.windows.filesystem_notifications import (
    FilesystemMonitor,
    NotifyProcessor as _GeneralINotifyProcessor,
)
from ubuntuone.platform.windows import notification
from ubuntuone.platform.windows.ipc import (
    IPCInterface as ExternalInterface,
    is_already_running,
)
