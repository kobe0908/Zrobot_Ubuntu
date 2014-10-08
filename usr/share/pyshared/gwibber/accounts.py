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
# Accounts interface for Gwibber
#

from gi.repository import Gdk, GdkPixbuf, Gtk, Pango

import gettext
from gettext import lgettext as _
if hasattr(gettext, 'bind_textdomain_codeset'):
  gettext.bind_textdomain_codeset('gwibber','UTF-8')
gettext.textdomain('gwibber')

import os, json, uuid
from gwibber.lib import GwibberPublic
from gwibber.util import get_service_icon
from gwibber.microblog.util import keyring, resources

for p in resources.get_plugin_dirs()[0]:
  print "Loading plugin for %s" % p
  globals()[p] = __import__("%s.gtk.%s" % (p,p), fromlist='*')


from dbus.mainloop.glib import DBusGMainLoop
DBusGMainLoop(set_as_default=True)


import subprocess
state_interface = "org.gwibber.state"
settings_interface = "org.gwibber.preferences"

class GwibberAccountManager(object):
  def __init__(self, selected_account=None, condition=None, message=None):
    self.icon_theme = Gtk.IconTheme.get_default ()
    self.icon_theme.prepend_search_path ("/usr/share/gwibber/ui/icons/")
    if os.path.exists(os.path.join("data", "icons")):
      self.icon_theme.prepend_search_path (os.path.realpath(os.path.join("data", "icons")))

    self.selected_account = []
    if selected_account:
      self.selected_account = selected_account.split(",")
    self.condition = condition
    self.message = message
    self.gwibber = GwibberPublic()
    self.services = json.loads(self.gwibber.GetServices())
    self.ui = Gtk.Builder()
    self.ui.set_translation_domain("gwibber")
    self.ui.add_from_file(resources.get_ui_asset("gwibber-accounts-dialog.ui"))
    self.ui.connect_signals(self)

    self.dialog = self.ui.get_object("accounts_dialog")
    self.dialog.resize(640,400)
    self.dialog.set_icon_name("gwibber")
    self.dialog.set_wmclass("gwibber", "Gwibber")
    self.dialog.show_all()
    if hasattr(Gtk, "InfoBar"):
      self.alignment_infobar = self.ui.get_object("alignment_infobar")
      self.infobar = Gtk.InfoBar()
      self.alignment_infobar.add(self.infobar)
      self.infobar.hide()

    # Hide the help button until we have help :)
    button_help = self.ui.get_object("button_help")
    button_help.hide()

    # This should check for configured accounts, and if there are any hide this
    self.ui.get_object('frame_new_account').hide()
    self.ui.get_object('vbox_save').hide()
    self.ui.get_object('vbox_create').hide()
    
    self.setup_account_tree()
    self.populate_account_tree()
    
  def setup_account_tree(self):
    # Protocol title, Icon, Protocol Properties
    self.service_store = Gtk.ListStore(str, GdkPixbuf.Pixbuf, str)
    for name, props in self.services.items():
      icon = self.get_icon(name)
      if icon:
        self.service_store.append((props["name"], icon, name))

    service_combo = self.ui.get_object("protocol_combobox")
    service_combo.set_model(self.service_store)

    celltxt = Gtk.CellRendererText()
    cellimg = Gtk.CellRendererPixbuf()
    
    service_combo.pack_start(cellimg, False)
    service_combo.pack_start(celltxt, False)
    service_combo.add_attribute(cellimg, "pixbuf", 1)
    service_combo.add_attribute(celltxt, "text", 0)
    service_combo.set_active(0)

    # Store: Account name, Icon, Protocol properties, Color
    self.account_store = Gtk.TreeStore(str, GdkPixbuf.Pixbuf, object, str)

    icon_column = Gtk.TreeViewColumn('Icon')
    name_column = Gtk.TreeViewColumn('Account')

    celltxt = Gtk.CellRendererText()
    cellimg = Gtk.CellRendererPixbuf()

    icon_column.pack_start(cellimg, False)
    icon_column.add_attribute(cellimg, 'pixbuf', 1)
    icon_column.add_attribute(cellimg, 'cell-background', 3)
    
    name_column.pack_start(celltxt, True)
    name_column.add_attribute(celltxt, 'text', 0)
    name_column.add_attribute(celltxt, 'cell-background', 3)
    
    self.account_tree = self.ui.get_object("accounts_tree")
    self.account_tree.append_column(icon_column)
    self.account_tree.append_column(name_column)
    self.account_tree.set_model(self.account_store)

  def select_account(self):
    column = self.account_tree.get_column(0)
    if len(self.selected_account) < 1:
      if len(self.account_store):
        self.account_tree.set_cursor(Gtk.TreePath.new_from_string('0'),
                                     column, False)
      else: self.add_account()
    else:
      for i in self.account_store:
        if len(self.selected_account) > 0:
          if i[2]["id"] == self.selected_account[0]:
            self.account_tree.set_cursor(i.path, column, False)

  def get_icon(self, name):
    try:
      icon = self.icon_theme.load_icon (name, 16, 0)
    except:
      icon_path = os.path.join("gwibber", "microblog", "plugins", name, "ui", "icons")
      if os.path.exists(icon_path):
        self.icon_theme.prepend_search_path (os.path.realpath(icon_path))
        icon = self.icon_theme.load_icon (name, 16, 0)
      else:
        icon = self.icon_theme.load_icon ("gwibber", 16, 0)
    return icon

  def populate_account_tree(self):
    self.account_store.clear()
    accounts = json.loads(self.gwibber.GetAccounts())
    for account in accounts:
        try:
          icon = self.get_icon(account["service"])
          if account.has_key("site_display_name"):
            name = account["site_display_name"]
          else:
            name = "%s (%s)" % (self.services[account["service"]]["name"], account["username"])
          private_fields = [f.split(":")[-1] for f in self.services[account["service"]]["config"] if ":" in f]
          color = None
          for f in private_fields:
            if not account.has_key(f) or account[f] is None: account[f] = ":KEYRING:MISSING"
            if account[f].startswith(":KEYRING:"):
              value = keyring.get_from_keyring(account["id"], f)
              if value is None or account[f] == ":KEYRING:MISSING":
                color = "pink"
                if account["id"] not in self.selected_account:
                  self.selected_account.append (account["id"])
                  self.condition = "error"
          self.account_store.append(None, [name, icon, account, color])
        except:
          pass
    self.select_account()

  def verify_account(self, account):
    for field in self.services[account["service"]]["config"]:
      if field.split(":")[-1] not in account:
        print "Couldn't find field:", field.split(":")[-1]
        return False
    return True

  def on_edit_account(self, widget, data=None):
    if "id" not in self.account: return

    self.on_edit_account_save()
    #self.ui.get_object('vbox_save').show()
    #self.ui.get_object('vbox_create').hide()

  def on_edit_account_cancel(self, widget):
    #self.ui.get_object('vbox_save').hide()
    #self.ui.get_object('vbox_create').hide()
    self.select_account()

  def on_account_delete(self, widget):
    if not hasattr(self, 'account'):
      pass
    else:  
      if "id" in self.account:
        print self.account['id']
        try:
          private_fields = [f.split(":")[-1] for f in self.services[self.account["service"]]["config"] if ":" in f]
          for f in private_fields:
            if self.account[f].startswith(":KEYRING:"):
              keyring_id = int(self.account[f].split(":")[-1])
              keyring.del_from_keyring(keyring_id)
        except:
          pass  
        self.gwibber.accounts.Delete(self.account["id"])
      self.populate_account_tree()

  def on_edit_account_save(self, widget=None):
    service = self.services[self.account["service"]]
    is_new = "id" not in self.account

    if is_new: self.account["id"] = uuid.uuid1().hex
    
    for config in service["config"]:
      is_private = config.startswith("private:")
      config = config.replace("private:", "")
      widget = self.account_widget.ui.get_object(config)

      value = None

      for p in ["text", "active"]:
        if widget and hasattr(widget.props, p):
          value = getattr(widget.props, p)
          self.account[config] = value

      if widget and isinstance(widget, Gtk.ColorButton):
        value = widget.get_color()
        self.account[config] = value.to_string()

      if is_private and self.account.has_key(config):
        if not self.account[config].startswith(":KEYRING:"):
	  self.account[config] = ":KEYRING:%s" % keyring.put_in_keyring(
	      self.account["id"], config, self.account[config])

      if value:
        if isinstance(value, Gdk.Color):
          self.account[config] = value.to_string()

    if not self.verify_account(self.account): return False

    fn = "Create" if is_new else "Update"
    getattr(self.gwibber.accounts, fn)(json.dumps(self.account))

    self.ui.get_object('vbox_save').hide()
    self.ui.get_object('vbox_create').hide()

    # if we just fixed a failure case, hide the infobar
    if self.account["id"] in self.selected_account:
      if hasattr(Gtk, "InfoBar") and len(self.selected_account) <= 1:
        self.infobar.hide()
      self.selected_account.remove (self.account["id"])

    self.populate_account_tree()

    # Set the autostart gsettings key so we get loaded on login
    state = subprocess.Popen(['gsettings', 'get', state_interface, 'run'], stdout=subprocess.PIPE)
    res = state.communicate()[0]
    if "false" in res:
      subprocess.call(['gsettings', 'set', state_interface, 'run', 'true'])
      subprocess.call(['gsettings', 'set', settings_interface, 'autostart', 'true'])

    return True

  def on_button_add_activate(self, widget=None, data=None):
    self.add_account()

  def add_account(self):
    # Populate protocols combobox
    self.ui.get_object('frame_new_account').show()
    self.ui.get_object('vbox_details').hide()
    self.ui.get_object('vbox_account').hide()
    self.ui.get_object('vbox_save').hide()
    self.ui.get_object('vbox_create').hide()

  def on_button_create_clicked(self, widget, data=None):
    model = widget.get_model()
    iter = widget.get_active_iter()
    if not iter:
        return  # None is selected
    icon = model.get_value(iter, 1)
    service = model.get_value(iter, 2)
    self.account_show(service, icon)

  def account_show(self, service_id, icon=None, account=None, condition=None, message=None):
    if hasattr(Gtk, "InfoBar"):
      if condition == "error":
        self.infobar.set_message_type(Gtk.MessageType.ERROR)
      if condition == "info":
        self.infobar.set_message_type(Gtk.MessageType.INFO)
      if message and condition:
        if hasattr(self, "infobar_content_area"):
          for child in self.infobar_content_area.get_children(): child.destroy()
        self.infobar_content_area = self.infobar.get_content_area()
        message_label = Gtk.Label(message)
        message_label.set_use_markup(True)
        message_label.set_ellipsize(Pango.EllipsizeMode.END)
        self.infobar_content_area.add(message_label)
        self.infobar.show_all()
      else:
        self.infobar.hide()

    vbox_account = self.ui.get_object('vbox_account')
    for child in vbox_account.get_children(): child.destroy()

    self.ui.get_object('vbox_details').show()
    self.ui.get_object('vbox_account').show()
    self.ui.get_object('frame_new_account').hide()

    service = self.services[service_id]
    self.ui.get_object('label_name').set_label(service["name"])

    if icon:
      self.ui.get_object('image_type').set_from_pixbuf(self.get_icon(service_id))

    if service_id in globals():
      if not account:
        account = {"service": service_id}
        is_new = True
      else:
        is_new = False

      aw = globals()[service_id].AccountWidget(account, self)

      vbox_account.pack_start(aw, False, False, 0)
      vbox_account.show()

      if "color" not in account:
        account["color"] = service["color"]

      for config in service["config"]:
        is_private = config.startswith("private:")
        config = config.replace("private:", "")

        if config in account:
          value = account[config]
          widget = aw.ui.get_object(config)
          
          if isinstance(widget, Gtk.Entry):
            if is_private and account[config].startswith(":KEYRING:"):
              value = keyring.get_from_keyring(account["id"], config)
              if not value:
                widget.modify_base(Gtk.StateType.NORMAL, Gdk.Color.parse("pink")[1])
            if value:
              widget.set_text(value)
            widget.connect("changed", self.on_edit_account)

          elif isinstance(widget, Gtk.CheckButton):
            widget.set_active(value)
            widget.connect("toggled", self.on_edit_account)

          elif isinstance(widget, Gtk.ColorButton):
            parsed, color = Gdk.Color.parse(value)
            widget.set_color(color)
            widget.connect("color-set", self.on_edit_account)

      self.account = account
      self.account_widget = aw
    if not is_new:
      self.ui.get_object('vbox_create').hide()

  def on_accounts_dialog_destroy(self, widget, data=None):
    Gtk.main_quit()

  def on_accounts_tree_row_activated(self, widget, data=None):
    self.ui.get_object('vbox_save').hide()
    self.ui.get_object('vbox_create').hide()

    selection = widget.get_selection()
    rows, model = (None, None)
    if selection:
      model, rows = selection.get_selected_rows()

    if rows and model:
      iter = model.get_iter(rows[0])
      icon = model.get_value(iter, 1)
      acct = model.get_value(iter, 2)
      if acct["id"] in self.selected_account and self.condition:
        self.account_show(acct["service"], icon, acct, self.condition, self.message)
      else:
        self.account_show(acct["service"], icon, acct)

  def on_button_close_clicked(self, widget, data=None):
    Gtk.main_quit()
