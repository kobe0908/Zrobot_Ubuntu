# ubuntuone.platform.linux.event_logging
#
# Author: Alejandro J. Cura <alecu@canonical.com>
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
"""Builds a syncdaemon listener that logs events if ZG is installed."""


def is_zeitgeist_installed():
    """Return true if zeitgeist is installed."""
    try:
        import zeitgeist
        import zeitgeist.mimetypes
        # use the above module in some way so pylint does not complain
        assert(zeitgeist is not None)
        return True
    except (ImportError, AttributeError):
        return False


def get_listener(fsm, vm):
    """Build a listener if zg is installed."""
    if is_zeitgeist_installed():
        from ubuntuone.eventlog import zg_listener
        return zg_listener.ZeitgeistListener(fsm, vm)
    else:
        return None
