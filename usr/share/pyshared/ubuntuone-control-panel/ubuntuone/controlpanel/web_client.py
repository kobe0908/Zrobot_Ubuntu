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

"""The web client."""

import simplejson

from twisted.internet import defer
# need to export the exceptions to avoid API breakage
# pylint: disable=W0611
from ubuntu_sso.utils.webclient import (
    UnauthorizedError,
    WebClientError,
    webclient_factory,
)
# pylint: enable=W0611

from ubuntuone.controlpanel import WEBSERVICE_BASE_URL
from ubuntuone.controlpanel.logger import setup_logging
from ubuntuone.platform.credentials import APP_NAME

logger = setup_logging('webclient')


class WebClient(object):
    """A client for the u1 webservice."""

    def __init__(self, get_credentials, base_url=WEBSERVICE_BASE_URL):
        """Initialize the webclient."""
        self.base_url = base_url
        self.get_credentials = get_credentials
        self.wc = webclient_factory(APP_NAME)
        logger.debug("WebClient created: base_url is %r, inner client is %r.",
                     self.base_url, self.wc)

    @defer.inlineCallbacks
    def call_api(self, api_name, extra_headers=None):
        """Call the webservice."""
        # this may log device ID's, but only for removals, which is OK
        logger.debug("calling api: %r", api_name)
        iri = self.base_url + api_name
        credentials = yield self.get_credentials()
        response = yield self.wc.request(iri, extra_headers=extra_headers,
                                     oauth_credentials=credentials)
        result = simplejson.loads(response.content)
        defer.returnValue(result)

    @defer.inlineCallbacks
    def build_signed_iri(self, iri, params=None):
        """Build an OAuth iri."""
        credentials = yield self.get_credentials()
        result = yield self.wc.build_signed_iri(iri, credentials, params)
        defer.returnValue(result)

    def shutdown(self):
        """Shutdown and cleanup."""
        return self.wc.shutdown()
