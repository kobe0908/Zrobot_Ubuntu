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

"""The control panel UI for Ubuntu One."""

import gettext

# pylint: disable=W0611
from ubuntuone.clientdefs import APP_NAME
# pylint: enable=W0611

from ubuntuone.controlpanel import TRANSLATION_DOMAIN
from ubuntuone.controlpanel.backend import UBUNTUONE_LINK


gettext.install(TRANSLATION_DOMAIN, unicode=True)


ERROR_COLOR = u'red'
KILOBYTES = 1024
FREE_ACCOUNT_SIZE = (KILOBYTES ** 3) * 5  # 5 gigs
NO_OP = lambda *a, **kw: None
# http://design.canonical.com/the-toolkit/ubuntu-logo-and-circle-of-friends/
ORANGE = u'#DD4814'
QUOTA_THRESHOLD = 0.95
QUOTA_THRESHOLD_ACCOUNTS = {
    'free': FREE_ACCOUNT_SIZE * 0.1,  # 10% of the free account size
    'pay': (KILOBYTES ** 3) * 3}  # 3 gigs
SHARES_MIN_SIZE_FULL = 1048576
SUCCESS_COLOR = u'green'

ERROR_ICON = u'✘'
SYNCING_ICON = u'⇅'
IDLE_ICON = u'✔'

CONTACT_ICON_NAME = u'avatar-default'
FOLDER_ICON_NAME = u'folder'
SHARE_ICON_NAME = u'folder-remote'
MUSIC_ICON_NAME = u'audio-x-generic'

CONTACTS_ICON = u'contacts.png'
FACEBOOK_LOGO = u'facebook.png'
FILES_ICON = u'files.png'
OVERVIEW_BANNER = u'overview.png'
TWITTER_LOGO = u'twitter.png'
MUSIC_STORE_ICON = u'music-store.png'
MUSIC_STREAM_ICON = u'music-stream.png'
NOTES_ICON = u'notes.png'
SERVICES_CONTACTS_ICON = u'services-contacts.png'
SERVICES_FILES_EXAMPLE = u'services-files-example.png'
SERVICES_FILES_ICON = u'services-files.png'

FILE_URI_PREFIX = u'file://'

CONTACTS_LINK = UBUNTUONE_LINK
EDIT_ACCOUNT_LINK = UBUNTUONE_LINK + u'account/'
EDIT_DEVICES_LINK = EDIT_ACCOUNT_LINK + u'machines/'
EDIT_PROFILE_LINK = u'https://login.ubuntu.com/'
EDIT_SERVICES_LINK = UBUNTUONE_LINK + u'services'
FACEBOOK_LINK = u'http://www.facebook.com/ubuntuone/'
GET_STORAGE_LINK = UBUNTUONE_LINK + u'services/#storage_panel'
GET_SUPPORT_LINK = UBUNTUONE_LINK + u'support/'
LEARN_MORE_LINK = UBUNTUONE_LINK
MANAGE_FILES_LINK = UBUNTUONE_LINK + u'files/'
RESET_PASSWORD_LINK = EDIT_PROFILE_LINK + u'+forgot_password'
TWITTER_LINK = u'http://twitter.com/ubuntuone/'

# Undefined variable '_', pylint: disable=E0602
# Translatable strings

ACCOUNT_LABEL = _('Your services')
ALWAYS_SUBSCRIBED = _('Always in sync')
ARE_YOU_SURE_HELP = _('If you need to know more about Ubuntu One, then '
    'please go to {support_url}')
ARE_YOU_SURE_NO = _('No, continue setting up')
ARE_YOU_SURE_SUBTITLE = _('You can restart the setup process at any time '
    'by clicking on Ubuntu One in your menu.')
ARE_YOU_SURE_TITLE = _('Are you sure you want to cancel setting up '
    'Ubuntu One?')
ARE_YOU_SURE_YES = _('Yes, I want to cancel')
CLOUD_TO_COMPUTER_SUBTITLE = _('These are the folders in your cloud. '
    'Select the ones you want to sync with this computer.')
CLOUD_TO_COMPUTER_TITLE = _('Syncing the cloud to your computer')
COMPUTER_TO_CLOUD_SUBTITLE = _('Okay! Now it\'s time to choose which folders '
    'on this computer you would like to sync to the cloud.')
COMPUTER_TO_CLOUD_TITLE = _('Syncing your computer with the cloud')
CONNECT_BUTTON_LABEL = _('Connect to Ubuntu One')
CONTACTS = _('Thunderbird plug-in')
CREDENTIALS_ERROR = _('There was a problem while retrieving the credentials.')
DASHBOARD_BUTTON_TOOLTIP = _('View your personal details and service '
                             'summary')
DASHBOARD_TITLE = WELCOME_LABEL = _('Welcome to Ubuntu One!')
DASHBOARD_VALUE_ERROR = _('The information could not be retrieved. '
                          'Maybe your internet connection is down?')
DESKTOPCOUCH_PKG = 'desktopcouch-ubuntuone'
DEVICE_CHANGE_ERROR = _('The settings could not be changed,\n'
                        'previous values were restored.')
DEVICE_CONFIRM_REMOVE = _('Are you sure you want to remove this device '
                          'from Ubuntu One?')
DEVICE_REMOVABLE_PREFIX = u'Ubuntu One @ '
DEVICE_REMOVAL_ERROR = _('The device could not be removed.')
DEVICES_BUTTON_TOOLTIP = _('Manage devices registered with your personal '
                           'cloud')
DEVICES_LOCAL_LABEL = _('This device')
DEVICES_MANAGE_LABEL = _('Go to the web page to manage your other devices')
DEVICES_REMOTE_LABEL = _('Other devices')
DEVICES_TITLE = _('The devices connected with your personal cloud are listed '
                  'below.')
EDIT_ACCOUNT_LABEL = _('Edit your services  online')
EDIT_PROFILE_LABEL = _('Edit personal details online')
FAILED_INSTALL = _('<i>%(package_name)s</i> could not be installed')
FOLDER_ADD_BUTTON_TEXT = _('Sync another folder with your cloud')
FOLDER_INVALID_PATH = _('The chosen directory "%(folder_path)s" is not valid. '
                        '\n\n'
                        'Please choose a folder inside your "%(home_folder)s" '
                        'directory, and not overlapping with any existing '
                        'cloud folder.')
FOLDER_OWNED_BY = _('My personal folders')
FOLDER_SHARED_BY = _('Shared by %(other_user_display_name)s')
FOLDERS_BUTTON_ADD_FOLDER = _('Add a folder from this computer')
FOLDERS_BUTTON_TOOLTIP = VOLUMES_BUTTON_TOOLTIP = _('Manage your cloud '
                                                     'folders')
FOLDERS_COLUMN_EXPLORE = _('Explore')
FOLDERS_COLUMN_NAME = _('Name')
FOLDERS_COLUMN_SYNC_LOCALLY = _('Sync Locally?')
FOLDERS_CONFIRM_MERGE = _('The contents of your cloud folder will be merged '
                          'with your local folder "%(folder_path)s" when '
                          'subscribing.\nDo you want to subscribe to this '
                          'cloud folder?')
FOLDERS_MANAGE_LABEL = _('Go to the web for public and private sharing '
    'options')
FOLDERS_TITLE = _('Select which folders from your cloud you want to sync with '
  'this computer')
FILE_SYNC_CONNECT = _('Connect')
FILE_SYNC_CONNECT_TOOLTIP = _('Connect the file sync service with '
                              'your personal cloud')
FILE_SYNC_DISABLED = _('File Sync is disabled.')
FILE_SYNC_DISCONNECT = _('Disconnect')
FILE_SYNC_DISCONNECT_TOOLTIP = _('Disconnect the file sync service from '
                                 'your personal cloud')
FILE_SYNC_DISCONNECTED = _('File Sync is disconnected.')
FILE_SYNC_ENABLE = _('Enable')
FILE_SYNC_ENABLE_TOOLTIP = _('Enable the file sync service')
FILE_SYNC_ERROR = _('File Sync error.')
FILE_SYNC_IDLE = _('File Sync is up-to-date.')
FILE_SYNC_RESTART = _('Restart')
FILE_SYNC_RESTART_TOOLTIP = _('Restart the file sync service')
FILE_SYNC_SERVICE_NAME = _('File Sync')
FILE_SYNC_START = _('Start')
FILE_SYNC_START_TOOLTIP = _('Start the file sync service')
FILE_SYNC_STARTING = _('File Sync starting...')
FILE_SYNC_STOP = _('Stop')
FILE_SYNC_STOP_TOOLTIP = _('Stop the file sync service')
FILE_SYNC_STOPPED = _('File Sync is stopped.')
FILE_SYNC_SYNCING = _('File Sync in progress...')
FREE_SPACE_TEXT = _('%(free_space)s available storage')
GENERAL_ERROR_TITLE = _('Ubuntu One experienced an error')
GENERAL_ERROR_MSG = _('Sorry, an error has occurred and Ubuntu One '
                      'needs to close.')
GET_HELP_ONLINE = _('Get help online')
GET_MORE_STORAGE = _('Get more storage')
GREETING = _('Hi %(user_display_name)s')
INSTALL = _('Install')
INSTALL_PACKAGE = _('You need to install the package <i>%(package_name)s'
                    '</i> in order to enable more sync services.')
INSTALL_PLUGIN = _('Install the %(plugin_name)s for the sync service: '
                   '%(service_name)s')
INSTALLING = _('Installation of <i>%(package_name)s</i> in progress')
LICENSE_AGREE = _('Agree and continue')
LICENSE_AGREEMENT = _('License Agreement')
LICENSE_BASIC = _('Ubuntu One Basic is free, while additional service add-ons '
    'may be paid for services.')
LICENSE_DISAGREE = _('Disagree and uninstall')
LICENSE_GPL3 = _('This program is free software: you can redistribute it '
    'and/or modify it under the terms of the GNU General Public License '
    'version 3, as published by the Free Software Foundation.')
LICENSE_LINK = _('As free software, this programme is distributed without '
    'warranty. See the GNU General Public License for more details at '
    '{license_link}')
LOADING = _('Loading...')
LOADING_OVERLAY = _('Getting information, please wait...')
LOCAL_FOLDERS_CALCULATING = _('Calculating...')
LOCAL_FOLDERS_OVERFLOW = _('The folders you have selected to sync take '
    'over your {quota_total} space. '
    'You can remove some folders or add some extra storage.')
LOCAL_FOLDERS_FOLDER_HEADER = _('Sync these folders on my computer')
LOCAL_FOLDERS_SPACE_HEADER = _('Space {space_total}')
MAIN_ACCOUNT_TAB = _('Account information')
MAIN_DEVICES_TAB = _('Devices')
MAIN_FOLDERS_TAB = _('Folders')
MAIN_PREFERENCES_TAB = _('Settings')
MAIN_WINDOW_TITLE = _('%(app_name)s Control Panel')
MUSIC_DISPLAY_NAME = _('Purchased Music')
MUSIC_REAL_PATH = u'.ubuntuone/Purchased from Ubuntu One'
MY_FOLDERS = _('My folders')
NAME_NOT_SET = _('[unknown user name]')
NETWORK_OFFLINE = _('An internet connection is required to join or sign '
                    'in to %(app_name)s.')
NO_DEVICES = _('No devices to show.')
NO_FOLDERS = _('No folders to show.')
NO_PAIRING_RECORD = _('There is no Ubuntu One pairing record.')
PERCENTAGE_LABEL = _('%(percentage)s used')
PLEASE_WAIT = _('Please wait')
PROFILE_LABEL = _('Personal details')
QUOTA_LABEL = _('Using %(used)s of %(total)s (%(percentage).0f%%)')
REMOVE_BUTTON = _('Remove')
RESTORE_LABEL = _('Restore')
SELECT_FOLDERS = _('Select sync folders')
SERVICES_BUTTON_TOOLTIP = _('Manage the sync services')
SERVICES_TITLE = _('Enable the sync services for this computer.')
SETTINGS_ALLOW_NOTIFICATIONS = _('Allow all notifications to this device')
SETTINGS_AUTO_CONNECT = _('Connect automatically when computer starts')
SETTINGS_BANDWIDTH = _('Bandwidth Settings')
SETTINGS_BANDWIDTH_ZERO_WARNING = _('Please note that your files will not '
    'sync if you set bandwidth to 0')
SETTINGS_BUTTON_APPLY = _('Apply these settings')
SETTINGS_BUTTON_DEFAULT = _('Default settings')
SETTINGS_CHANGE_ERROR = _('The settings could not be changed,\n'
                          'previous values were restored.')
SETTINGS_FILE_SYNC = _('File Sync Settings')
SETTINGS_KILOBITS_PER_SECOND = _('Kilobits per second')
SETTINGS_LIMIT_DOWNLOAD = _('Limit download speed to')
SETTINGS_LIMIT_UPLOAD = _('Limit upload speed to')
SETTINGS_SYNC_ALL_FOLDERS = _('Automatically sync all new cloud folders '
    'to this computer')
SETTINGS_SYNC_ALL_SHARES = _('Automatically sync all folders shared with me '
    'to this computer')
SHARES_BUTTON_TOOLTIP = _('Manage the shares offered to others')
SHARES_TITLE = _('Manage permissions for shares made to other users.')
SIGN_IN = _('Sign in')
SUCCESS_INSTALL = _('<i>%(package_name)s</i> was successfully installed')
SYNC_STREAM_SHARE = _('Sync, stream, share')
TALK_TO_US = _('Talk to us')
VALUE_ERROR = _('Value could not be retrieved.')
UNKNOWN_ERROR = _('Unknown error')
USAGE_LABEL = _('%(used)s of %(total)s')
# TODO: mark the following strings translatable after precise is released
UPDATE_TITLE = APP_NAME
UPDATE_SOFTWARE = ('There is a new update available.'
                   ' Would you like to install it?')
QUIT_LABEL = _('Quit Ubuntu One')

# pylint: enable=E0602


def humanize(int_bytes):
    """Return a human readable representation of 'int_bytes'.

    This method follows the https://wiki.ubuntu.com/UnitsPolicy to build
    the result.

    """
    units = {0: 'bytes', 1: 'KiB', 2: 'MiB', 3: 'GiB', 4: 'TiB',
             5: 'PiB', 6: 'Eib', 7: 'ZiB', 8: 'YiB'}
    unit = 0
    while int_bytes >= KILOBYTES:
        int_bytes = int_bytes / float(KILOBYTES)
        unit += 1
    str_bytes = "%.1f" % int_bytes
    str_bytes = str_bytes.rstrip('0')
    str_bytes = str_bytes.rstrip('.')
    return '%s %s' % (str_bytes, units[unit])


def show_quota_warning(int_bytes_used, int_bytes_total):
    """Return True if the user should be warn about the remaining quota."""
    available = (int_bytes_total - int_bytes_used)
    free_threshold = (int_bytes_total == FREE_ACCOUNT_SIZE and
                      available <= QUOTA_THRESHOLD_ACCOUNTS['free'])
    payed_threshold = (int_bytes_total > FREE_ACCOUNT_SIZE and
                       available <= QUOTA_THRESHOLD_ACCOUNTS['pay'])

    return free_threshold or payed_threshold
