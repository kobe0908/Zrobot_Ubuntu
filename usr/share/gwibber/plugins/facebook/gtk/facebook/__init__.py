#
# Copyright (C) 2010 Canonical Ltd
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Copyright (C) 2010 Ken VanDine <ken.vandine@canonical.com>
#
# facebook widgets for Gwibber
#

import urllib
import string

from gi.repository import Gdk, Gtk, WebKit, Pango
from gi.repository.Gtk import Builder
from gwibber.microblog.util import resources
from gwibber.microblog.util.const import *
from gwibber.microblog.util.keyring import get_from_keyring
# Try to import * from custom, install custom.py to include packaging 
# customizations like distro API keys, etc
try:
  from gwibber.microblog.util.custom import *
except:
  pass

import json, urlparse, uuid
import gettext
from gettext import gettext as _
if hasattr(gettext, 'bind_textdomain_codeset'):
    gettext.bind_textdomain_codeset('gwibber','UTF-8')
gettext.textdomain('gwibber')

"""
Gdk.threads_init()

APP_KEY = "71b85c6d8cb5bbb9f1a3f8bbdcdd4b05"
"""

class AccountWidget(Gtk.VBox):
  """AccountWidget: A widget that provides a user interface for configuring facebook accounts in Gwibber
  """
  
  def __init__(self, account=None, dialog=None):
    """Creates the account pane for configuring facebook accounts"""
    Gtk.VBox.__init__( self, False, 20 )
    self.ui = Gtk.Builder()
    self.ui.set_translation_domain ("gwibber")
    self.ui.add_from_file (resources.get_ui_asset("gwibber-accounts-facebook.ui"))
    self.ui.connect_signals(self)
    self.vbox_settings = self.ui.get_object("vbox_settings")
    self.pack_start(self.vbox_settings, False, False, 0)
    self.show_all()
    if account:
      self.account = account
    else:
      self.account = {}
    self.dialog = dialog
    self.window = dialog.dialog
    has_access_token = False
    if self.account.has_key("id"):
        has_secret_key = get_from_keyring(self.account['id'],
                                          'secret_token') is not None

    try:
      if self.account["access_token"] and self.account["username"] and has_access_token and not self.dialog.condition:
        self.ui.get_object("hbox_facebook_auth").hide()
        self.ui.get_object("fb_auth_done_label").set_label(_("%s has been authorized by Facebook") % str(self.account["username"]))
        self.ui.get_object("hbox_facebook_auth_done").show()
      else:
        self.ui.get_object("hbox_facebook_auth_done").hide()
        if self.dialog.ui:
          self.dialog.ui.get_object('vbox_create').hide()
    except:
      self.ui.get_object("hbox_facebook_auth_done").hide()
      if self.dialog.ui:
        self.dialog.ui.get_object("vbox_create").hide()

  def console_message_cb (self, *args):
    return True

  def on_facebook_auth_clicked(self, widget, data=None):
    self.winsize = self.window.get_size()

    web = WebKit.WebView()
    web.get_settings().set_property("enable-plugins", False)
    web.get_settings().set_property("enable-developer-extras", False)
    web.connect("console-message", self.console_message_cb)
    web.load_html_string(_("<p>Please wait...</p>"), "file:///")

    url = urllib.urlencode({
      "client_id": FB_APP_KEY,
      "display": "popup",
      "type": "user_agent",
      "scope": "publish_stream,read_stream,status_update,offline_access,user_photos,friends_photos",
      "redirect_uri": "http://www.facebook.com/connect/login_success.html",
    })
    web.load_uri("https://graph.facebook.com/oauth/authorize?" + url)
    web.connect("title-changed", self.on_facebook_auth_title_change)

    self.scroll = Gtk.ScrolledWindow()
    
    self.scroll.add(web)
    self.scroll.set_size_request(450, 340)

    self.pack_start(self.scroll, True, True, 0)
    self.show_all()
    self.dialog.infobar.hide()
    self.ui.get_object("vbox1").hide()
    self.ui.get_object("vbox_advanced").hide()

  def on_facebook_auth_title_change(self, web=None, title=None, data=None):
    saved = False
    if hasattr(self.dialog, "infobar_content_area"):
      for child in self.dialog.infobar_content_area.get_children(): child.destroy()
    self.dialog.infobar_content_area = self.dialog.infobar.get_content_area()
    self.dialog.infobar_content_area.show()

    url = web.get_main_frame().get_uri()
    if title.get_title() == "Success":
      try:
        self.account["access_token"] = str(urlparse.parse_qs(url.split("#", 1)[1])["access_token"][0])
      except:
        self.scroll.destroy()
        self.ui.get_object("vbox1").show()
        self.ui.get_object("vbox_advanced").show()
        self.window.resize(*self.winsize)
        self.dialog.select_account ()
        return

      message_label = Gtk.Label (_("Verifying"))
      message_label.set_use_markup(True)
      message_label.set_ellipsize(Pango.EllipsizeMode.END)
      self.dialog.infobar_content_area.add(message_label)
      self.dialog.infobar.show_all()
      self.scroll.destroy()

      data = json.loads(urllib.urlopen("https://graph.facebook.com/me?access_token=" + self.account["access_token"]).read())
      if isinstance(data, dict):
        if data.has_key("id") and data.has_key("name"):
          self.account["username"] = data["name"].encode("utf-8")
          self.account["uid"] = data["id"]
          saved = self.dialog.on_edit_account_save() 
      else:
        # Make a desparate attempt to guess the id from the url
        uid = url.split('-')[1].split('%7C')[0]
        if isinstance(uid, int) and len(uid) > 2:
          acct = json.loads(urllib.urlopen("https://graph.facebook.com/" + str(uid)).read())
          if isinstance(acct, dict):
            if acct.has_key("id") and acct.has_key("name"):
              self.account["uid"] = acct["id"]
              self.account["username"] = acct["name"].encode("utf-8")
              saved = self.dialog.on_edit_account_save()
          else:
            print "Failed"

      if saved:
        message_label.set_text(_("Successful"))
        self.dialog.infobar.set_message_type(Gtk.MessageType.INFO)

      self.ui.get_object("hbox_facebook_auth").hide()
      self.ui.get_object("fb_auth_done_label").set_label(_("%s has been authorized by Facebook") % str(self.account["username"]))
      self.ui.get_object("hbox_facebook_auth_done").show()
      if self.dialog.ui and self.account.has_key("id") and not saved:
        self.dialog.ui.get_object("vbox_save").show()
      elif self.dialog.ui and not saved:
        self.dialog.ui.get_object("vbox_create").show()

      self.ui.get_object("vbox1").show()
      self.ui.get_object("vbox_advanced").show()
      self.window.resize(*self.winsize)
      self.dialog.select_account ()

    if title.get_title() == "Failure":
      self.dialog.infobar.set_message_type(Gtk.MessageType.ERROR)
      message_label = Gtk.Label (_("Authorization failed. Please try again."))
      message_label.set_use_markup(True)
      message_label.set_ellipsize(Pango.EllipsizeMode.END)
      self.dialog.infobar_content_area.add(message_label)
      self.dialog.infobar.show_all()

      self.ui.get_object("vbox1").show()
      self.ui.get_object("vbox_advanced").show()
      self.scroll.destroy()
      self.window.resize(*self.winsize)
      self.dialog.select_account ()

