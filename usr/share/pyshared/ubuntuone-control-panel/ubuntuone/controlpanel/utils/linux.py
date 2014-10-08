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

"""Miscelaneous functions and constants for linux."""

import codecs
import os

from dirspec.basedir import xdg_config_home
from ubuntuone.controlpanel.logger import setup_logging


logger = setup_logging('utils.linux')


def default_folders(user_home='', dirs_path=None):
    """Return a list of the folders to add by default."""
    result = []

    if dirs_path is None:
        dirs_path = os.path.join(xdg_config_home, u'user-dirs.dirs')

    if not os.path.exists(dirs_path):
        logger.warning('default_folders: dirs_path %r does not exist.',
                       dirs_path)
        return result

    # pylint: disable=W0702

    try:
        with codecs.open(dirs_path, encoding='utf-8') as f:
            for line in f:
                if line.startswith(u'#'):
                    continue

                try:
                    _, value = line.strip().split(u'=')
                    value = value.strip(u'"').replace(u'$HOME', user_home)
                except:
                    logger.exception('default_folders: can not row %r:', line)
                else:
                    result.append(value)
    except:
        logger.exception('default_folders: can not load file %r:', dirs_path)

    return result
