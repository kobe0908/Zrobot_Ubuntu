#!/usr/bin/env python

import urllib, json
import urllib2, base64
import logging
logger = logging.getLogger("Network")

class UrlLib2Downloader:
  def __init__(self, url, params=None, post=False, username=None,
               password=None, header=None, body=None, proxy=None):

    data = None

    if params:
      if post:
        data = urllib.urlencode(params)
      else:
        url = "?".join((url, urllib.urlencode(params)))

    url = url.encode('utf-8')
    self.url = url

    if header:
      req = urllib2.Request(url, data, headers=header)
    else:
      req = urllib2.Request(url, data)

    if username and password:
      base64string = base64.encodestring('%s:%s' % (username, password)).replace('\n', '')
      req.add_header("Authorization", "Basic %s" % base64string)
    if proxy and len(proxy) > 1:  # If didn't get a list, we're screwed
      req.set_proxy(proxy[1], proxy[0])

    try:
      self.res = urllib2.urlopen(req)
    except urllib2.HTTPError, e:
      logger.error("HTTP Error for %s - error code: %s", e.geturl().split("?")[0], e.getcode())
      self.res = "HTTP error: {0}".format(e.getcode())
    except urllib2.URLError, e:
      logger.error("Network failure: %s", e.message)
      self.res = "Network error: {0}".format(e.message)
    except IOError, e:
      logger.error("Network failure: %s", e.message)
      self.res = "Network error: {0}".format(e.message)
    except:
      logger.error("Network failure: UNKNOWN")
      self.res = "Network error: UNKNOWN"

  def get_json(self):
    try:
      return json.loads(self.get_string())
    except ValueError as e:
      logger.debug("Failed to parse the response for %s, error was: %s", self.url.split("?")[0], str(e))
      return []

  def get_string(self):
    try:
      return self.res.read()
    except AttributeError:
      return self.res


Download = UrlLib2Downloader
