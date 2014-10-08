#!/usr/bin/python

try:
  from desktopcouch.records.server import CouchDatabase
  from desktopcouch.records.server_base import NoSuchDatabase
except:
  CouchDatabase = None
  
import string, subprocess, os
import sqlite3, uuid, json
from gwibber.lib import GwibberPublic

import resources
from gettext import lgettext as _

import logging
logger = logging.getLogger("Couch Migrate")

COUCH_DB_ACCOUNTS = "gwibber_accounts"

# Dynamically build a list of available service plugins
PROTOCOLS = {}
for p in resources.get_plugin_dirs()[0]:
    PROTOCOLS[str(p)] = __import__("%s" % p, fromlist='*')
    print "Loading plugin %s version %s" % (PROTOCOLS[str(p)].PROTOCOL_INFO["name"], PROTOCOLS[str(p)].PROTOCOL_INFO["version"])

SERVICES = dict([(k, v.PROTOCOL_INFO) for k, v in PROTOCOLS.items()])

class AccountCouchMigrate:
  def __init__(self):
    if CouchDatabase:
      self.gwibber = GwibberPublic()
      sqlite_accounts = json.loads(self.gwibber.GetAccounts())
    
      try:
        accounts = CouchDatabase(COUCH_DB_ACCOUNTS, create=False)
        records = accounts.get_records()
      except NoSuchDatabase:
        logger.info("Nothing to migrate from desktopcouch")
        return

      migrate = {}
      needs_auth = []

      logger.info("Looking for accounts to migrate from desktopcouch to sqlite")

      for record in records:
        id = str(record["value"]["protocol"] + "-" + record["value"]["username"])
        migrate[id] = True

        if len(sqlite_accounts) > 0:
          for sqlite_account in sqlite_accounts:
            if record["value"]["protocol"] == sqlite_account["service"] and record["value"]["username"] == sqlite_account["username"]:
              migrate[id] = False
        if not SERVICES.has_key(record["value"]["protocol"]):
          migrate[id] = False
        if migrate[id]:
          new_account = {}
          new_account["service"] = record["value"]["protocol"]
          new_account["id"] = record["value"]["_id"]
          for param in SERVICES[record["value"]["protocol"]]["config"]: 
            key = param.replace('private:','')
            new_account[key] = record["value"].get(key, None)
            if key == "access_token" and record["value"].has_key("secret_key"):
              new_account[key] = record["value"]["secret_key"]
            if (key == "secret_token" or key == "access_token") and new_account[key] is None and new_account["id"] not in needs_auth:
              needs_auth.append (new_account["id"])
            if key == "uid" and new_account[key] is None and new_account["id"] not in needs_auth:
              needs_auth.append (new_account["id"])
          logger.info("Found account %s - %s that needs to be migrated", new_account["service"], new_account["username"])
          self.gwibber.accounts.Create(json.dumps(new_account))
      logger.debug("ACCOUNTS NEED RE-AUTH: %s", needs_auth)
      if len(needs_auth) > 0:
        cmd = []
        cmd.append ("-a")
        cmd.append (string.join (needs_auth, ","))
        cmd.append ("-c")
        cmd.append ("info")
        cmd.append ("-m")
        cmd.append (_("Authorize"))
        if os.path.exists (os.path.join ("bin", "gwibber-accounts")):
          cmd.insert (0, os.path.join ("bin", "gwibber-accounts"))
        else:
          cmd.insert (0, "gwibber-accounts")
        process = subprocess.Popen (cmd)

AccountCouchMigrate()
