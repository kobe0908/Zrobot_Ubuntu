# -*- coding: utf-8 -*-
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
"""Utility modules that may find use outside ubuntu_sso."""

import cgi
import os
import sys
import time
import urllib2

from oauth import oauth
from urlparse import urlparse

from twisted.internet import defer

from ubuntu_sso.logger import setup_logging
from ubuntu_sso.utils import webclient


logger = setup_logging("ubuntu_sso.utils")
BIN_SUFFIX = 'bin'
DATA_SUFFIX = 'data'

if sys.platform == "win32":
    from ubuntu_sso.utils import windows as source
else:
    from ubuntu_sso.utils import linux as source
PLATFORM_QSS = source.PLATFORM_QSS


def _get_dir(dir_name, dir_constant):
    """Return the absolute path to this project's 'dir_name' dir.

    Support symlinks, and priorize local (relative) 'dir_name' dir. If not
    found, return the value of the 'dir_constant'.

    """
    module = os.path.dirname(__file__)
    result = os.path.abspath(os.path.join(module, os.path.pardir,
                                          os.path.pardir, dir_name))
    logger.debug('_get_dir: trying use dir at %r (exists? %s)',
                  result, os.path.exists(result))
    if os.path.exists(result):
        logger.info('_get_dir: returning dir located at %r.', result)
        return result

    # otherwise, try to load 'dir_constant' from installation path
    try:
        # Unused variable 'ubuntu_sso', pylint: disable=W0612, F0401, E0611
        import ubuntu_sso.constants
        module = sys.modules.get('ubuntu_sso.constants')
        return getattr(module, dir_constant)
    except (ImportError, AttributeError):
        msg = '_get_dir: can not build a valid path. Giving up. ' \
              '__file__ is %r, constants module not available.'
        logger.error(msg, __file__)


def get_project_dir():
    """Return the absolute path to this project's data/ dir.

    Support symlinks, and priorize local (relative) data/ dir. If not
    found, return the value of the PROJECT_DIR.

    """
    result = _get_dir(dir_name=DATA_SUFFIX, dir_constant='PROJECT_DIR')
    assert result is not None, '%r dir can not be None.' % DATA_SUFFIX
    return result


def get_data_file(*args):
    """Return the absolute path to 'args' within project data dir."""
    return os.path.join(get_project_dir(), *args)


def get_bin_dir():
    """Return the absolute path to this project's bin/ dir.

    Support symlinks, and priorize local (relative) bin/ dir. If not
    found, return the value of the BIN_DIR.

    """
    # If sys is frozen, this is an .exe, and all binaries are in
    # the same place
    if getattr(sys, "frozen", None) is not None:
        exec_path = os.path.abspath(sys.executable)
        result = os.path.dirname(exec_path)
    else:
        result = _get_dir(dir_name=BIN_SUFFIX, dir_constant='BIN_DIR')
    assert result is not None, '%r dir can not be None.' % BIN_SUFFIX
    logger.info('get_bin_dir: returning dir located at %r.', result)
    return result


class RequestHead(urllib2.Request):
    """A request with the method set to HEAD."""

    _request_method = "HEAD"

    def get_method(self):
        """Return the desired method."""
        return self._request_method


class SyncTimestampChecker(object):
    """A timestamp that's regularly checked with a server."""

    CHECKING_INTERVAL = 60 * 60  # in seconds
    ERROR_INTERVAL = 30  # in seconds
    SERVER_URL = "http://one.ubuntu.com/api/time"

    def __init__(self):
        """Initialize this instance."""
        self.next_check = time.time()
        self.skew = 0

    def get_server_time(self):
        """Get the time at the server."""
        headers = {"Cache-Control": "no-cache"}
        request = RequestHead(self.SERVER_URL, headers=headers)
        response = urllib2.urlopen(request)
        date_string = response.info()["Date"]
        # delay import, otherwise a default reactor gets installed
        from twisted.web import http
        timestamp = http.stringToDatetime(date_string)
        return timestamp

    def get_faithful_time(self):
        """Get an accurate timestamp."""
        local_time = time.time()
        if local_time >= self.next_check:
            try:
                server_time = self.get_server_time()
                self.next_check = local_time + self.CHECKING_INTERVAL
                self.skew = server_time - local_time
                logger.debug("Calculated server-local time skew: %r",
                             self.skew)
            #pylint: disable=W0703
            except Exception, server_error:
                logger.debug("Error while verifying the server time skew: %r",
                             server_error)
                self.next_check = local_time + self.ERROR_INTERVAL

        # delay import, otherwise a default reactor gets installed
        from twisted.web import http
        logger.debug("Using corrected timestamp: %r",
                     http.datetimeToString(local_time + self.skew))
        return int(local_time + self.skew)


# pylint: disable=C0103
timestamp_checker = SyncTimestampChecker()
# pylint: enable=C0103


def oauth_headers(url, credentials, http_method='GET'):
    """Sign 'url' using 'credentials'.

    * 'url' must be a valid unicode url.
    * 'credentials' must be a valid OAuth token.

    Return oauth headers that can be pass to any Request like object.

    """
    assert isinstance(url, unicode)
    url = url.encode('utf-8')
    _, _, _, _, query, _ = urlparse(url)
    parameters = dict(cgi.parse_qsl(query))
    parameters["oauth_timestamp"] = timestamp_checker.get_faithful_time()

    consumer = oauth.OAuthConsumer(credentials['consumer_key'],
                                   credentials['consumer_secret'])
    token = oauth.OAuthToken(credentials['token'],
                             credentials['token_secret'])
    kwargs = dict(oauth_consumer=consumer, token=token,
                  http_method=http_method, http_url=url,
                  parameters=parameters)
    get_request = oauth.OAuthRequest.from_consumer_and_token
    oauth_req = get_request(**kwargs)
    hmac_sha1 = oauth.OAuthSignatureMethod_HMAC_SHA1()
    oauth_req.sign_request(hmac_sha1, consumer, token)
    headers = oauth_req.to_header()

    return headers


@defer.inlineCallbacks
def ping_url(url, email, credentials):
    """Ping the 'url' with the 'email' attached to it.

    Sign the request with 'credentials'. The url must not be None.

    """
    logger.info('Pinging server using url: %r, email: %r.',
                url, email)
    assert isinstance(url, unicode), 'Url %r must be unicode' % url

    target_url = url
    try:
        target_url = url.format(email=email)
    except IndexError:  # tuple index out of range
        target_url = url.format(email)  # format the first substitution

    if target_url == url:
        logger.debug('Original url (%r) could not be formatted, '
                     'appending email (%r).', url, email)
        assert url.endswith(u'/'), 'Url %r must end with /.' % url
        target_url = url + email

    wc = webclient.webclient_factory()
    try:
        logger.debug('Opening the url %r with webclient.request.', url)
        response = yield wc.request(target_url, oauth_credentials=credentials)
        logger.debug('Url %r opened. Response content: %r.',
                     url, response.content)
        defer.returnValue(response)
    finally:
        wc.shutdown()
