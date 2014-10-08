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

"""Miscelaneous functions and constants for windows."""

import os
import sys

# Avoid pylint error on Linux
# pylint: disable=F0401
import win32api
import _winreg

from win32com.shell import shell, shellcon
# pylint: enable=F0401
from twisted.internet import defer
from twisted.internet.utils import getProcessValue

from ubuntuone.controlpanel.logger import setup_logging

logger = setup_logging('utils.windows')
AUTOUPDATE_EXE_NAME = 'autoupdate-windows.exe'
AUTORUN_KEY = r"Software\Microsoft\Windows\CurrentVersion\Run"
UNINSTALL_EXE_NAME = 'uninstall.exe'


def get_exe_path(exe_name):
    """Return the path in which the autoupdate command is found."""
    if getattr(sys, 'frozen', False):
        exec_path = os.path.abspath(sys.executable)
    else:
        exec_path = os.path.dirname(__file__)

    result = None
    folder = os.path.dirname(os.path.dirname(exec_path))
    exe_path = os.path.join(folder, exe_name)
    if os.path.exists(exe_path):
        result = exe_path

    return result


def add_to_autostart():
    """Add syncdaemon to the session's autostart."""
    if getattr(sys, "frozen", False):
        sd_path = '"%s"' % os.path.join(os.path.dirname(
            os.path.abspath(sys.executable)),
            "ubuntuone-syncdaemon.exe")
        u1cp_path = '"%s"' % os.path.join(os.path.dirname(
            os.path.abspath(sys.executable)),
            "ubuntuone-control-panel-qt.exe")

        with _winreg.OpenKey(_winreg.HKEY_CURRENT_USER, AUTORUN_KEY,
                             0, _winreg.KEY_ALL_ACCESS) as key:
            # pylint: disable=E0602
            _winreg.SetValueEx(key, "Ubuntu One", 0, _winreg.REG_SZ, sd_path)
            _winreg.SetValueEx(key, "Ubuntu One Icon", 0, _winreg.REG_SZ,
                               u1cp_path + " --minimized --with-icon")


@defer.inlineCallbacks
def are_updates_present():
    """Return if there are updates for Ubuntu One."""
    result = False
    retcode = None
    update_path = get_exe_path(exe_name=AUTOUPDATE_EXE_NAME)
    if update_path is not None:
        # If there is an update present we will get 0, non-zero otherwise
        retcode = yield getProcessValue(update_path, args=('--mode',
            'unattended'), path=os.path.dirname(update_path))
        result = retcode == 0
    logger.debug('are_updates_present: update path: %r, return code: %r,'
                 ' result: %r', update_path, retcode, result)
    defer.returnValue(result)


def default_folders(user_home=None):
    """Return a list of the folders to add by default."""
    # as per http://msdn.microsoft.com/en-us/library/windows/desktop/bb762181,
    # SHGetFolderPath is deprecated, we should migrate to SHGetKnownFolderPath
    # (http://msdn.microsoft.com/en-us/library/windows/desktop/bb762188)
    # but the latter does not support XP
    # (Minimum supported client: Windows Vista)
    get_path = lambda name: shell.SHGetFolderPath(
        0, getattr(shellcon, name), None, 0)

    folders = []
    # More information on these constants at
    # http://msdn.microsoft.com/en-us/library/bb762494
    for name in (u'PERSONAL', u'MYMUSIC', u'MYPICTURES', u'MYVIDEO'):
        name = u'CSIDL_%s' % name
        try:
            folders.append(get_path(name))
        except:  # pylint: disable=W0702
            logger.exception('default_folders: could not retrieve folder info '
                             'for name %r.', name)

    return folders


def perform_update():
    """Spawn the autoupdate process and call the stop function."""
    update_path = get_exe_path(exe_name=AUTOUPDATE_EXE_NAME)
    if update_path is not None:
        # lets call the updater with the commands that are required,
        win32api.ShellExecute(None, 'runas', update_path,
                              '--unattendedmodeui none', '', 0)


def uninstall_application():
    """Uninstall Ubuntu One."""
    uninstall_path = get_exe_path(exe_name=UNINSTALL_EXE_NAME)
    if uninstall_path is not None:
        win32api.ShellExecute(None, '', uninstall_path, '--mode win32', '', 0)
