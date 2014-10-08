from const import *
from gi.repository import GnomeKeyring, GLib

import ctypes
import exceptions


def get_from_keyring(acctid, name):
  """Get the entry from the keyring for @acctid with @name."""
  attributes = GnomeKeyring.Attribute.list_new()
  GnomeKeyring.Attribute.list_append_string(attributes, 'id',
                                            str("%s/%s" % (acctid, name)))
  result, value = GnomeKeyring.find_items_sync(
    GnomeKeyring.ItemType.GENERIC_SECRET,
    attributes)

  if result == GnomeKeyring.Result.OK:
    return value[0].secret

  return None


def put_in_keyring(acctid, name, value):
  """Store a value in the keyring."""
  id = "%s/%s" % (acctid, name)
  attributes = GnomeKeyring.Attribute.list_new()
  GnomeKeyring.Attribute.list_append_string(attributes, 'id', str(id))
  keyring = GnomeKeyring.get_default_keyring_sync()[1]
  value = GnomeKeyring.item_create_sync(
    keyring, GnomeKeyring.ItemType.GENERIC_SECRET,
    "Gwibber preference: %s" % id,
    attributes, str(value), True)
  return value[1]


def del_from_keyring(keyring_id):
  """Delete an entry from the keyring."""
  keyring = GnomeKeyring.get_default_keyring_sync()[1]
  GnomeKeyring.item_delete_sync(keyring, keyring_id)


def get_secret(id):
  """Get a locked secret for threaded/multiprocessing use."""
  value = ""
  attrlist = GnomeKeyring.Attribute.list_new()
  GnomeKeyring.Attribute.list_append_string(attrlist, 'id', str(id))
  result, found = GnomeKeyring.find_items_sync(
    GnomeKeyring.ItemType.GENERIC_SECRET,
    attrlist)
  if result == GnomeKeyring.Result.OK:
    value = found[0].secret
    mlock(value)
    return value
  elif result == GnomeKeyring.Result.NO_MATCH:
    print "FAILED: " + id
  return None


libc = ctypes.CDLL("libc.so.6")


def mlock(var):
    if var:
      libc.mlock(var, len(var))

def munlock(var):
    if var:
      libc.munlock(var, len(var))
