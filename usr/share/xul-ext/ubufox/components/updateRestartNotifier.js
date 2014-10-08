/* -*- Mode: javascript; tab-width: 2; indent-tabs-mode: nil; c-basic-offset: 2 -*- */
/* ***** BEGIN LICENSE BLOCK *****
 * Version: MPL 1.1/GPL 2.0/LGPL 2.1
 *
 * The contents of this file are subject to the Mozilla Public License Version
 * 1.1 (the "License"); you may not use this file except in compliance with
 * the License. You may obtain a copy of the License at
 * http://www.mozilla.org/MPL/
 *
 * Software distributed under the License is distributed on an "AS IS" basis,
 * WITHOUT WARRANTY OF ANY KIND, either express or implied. See the License
 * for the specific language governing rights and limitations under the
 * License.
 *
 * The Original Code is ubufox.
 *
 * The Initial Developer of the Original Code is
 * Canonical Ltd.
 * Portions created by the Initial Developer are Copyright (C) 2008
 * the Initial Developer. All Rights Reserved.
 *
 * Contributor(s):
 *   Alexander Sack <asac@jwsdot.com> - Canonical Ltd.
 *   Arzhel Younsi <xionox@gmail.com>
 *   Chris Coulson <chris.coulson@canonical.com>
 *
 * Alternatively, the contents of this file may be used under the terms of
 * either the GNU General Public License Version 2 or later (the "GPL"), or
 * the GNU Lesser General Public License Version 2.1 or later (the "LGPL"),
 * in which case the provisions of the GPL or the LGPL are applicable instead
 * of those above. If you wish to allow use of your version of this file only
 * under the terms of either the GPL or the LGPL, and not to allow others to
 * use your version of this file under the terms of the MPL, indicate your
 * decision by deleting the provisions above and replace them with the notice
 * and other provisions required by the GPL or the LGPL. If you do not delete
 * the provisions above, a recipient may use your version of this file under
 * the terms of any one of the MPL, the GPL or the LGPL.
 *
 * ***** END LICENSE BLOCK ***** */

const { classes: Cc, interfaces: Ci, utils: Cu } = Components;

Cu.import("resource://gre/modules/Services.jsm");
Cu.import("resource://gre/modules/XPCOMUtils.jsm");
Cu.import("resource://ubufox/Distro.jsm");

["LOG", "WARN", "ERROR"].forEach(function(aName) {
  this.__defineGetter__(aName, function() {
    Components.utils.import("resource://gre/modules/AddonLogging.jsm");

    LogManager.getLogger("ubufox.urn", this);
    return this[aName];
  });
}, this);

function UpdateRestartNotifier() {
  LOG("Starting");
  this.wrappedJSObject = this;

  var self = this;
  var listeners = [];
  var fired = false;
  var startupTime = Date.now();

  var timer = Cc["@mozilla.org/timer;1"].createInstance(Ci.nsITimer);

  function remindListeners() {
    listeners.forEach(function(listener) {
      try {
        listener.onUpdatedNotify();
      } catch(e) {
        Cu.reportError(e);
      }
    });
  }

  function notifyListeners() {
    try {
      timer.cancel();
      timer.initWithCallback(function() {
        remindListeners();
      }, 900000, Ci.nsITimer.TYPE_REPEATING_SLACK);
    } catch(e) {
      Cu.reportError(e);
    }

    fired = true;

    listeners.forEach(function(listener) {
      try {
        listener.onUpdatedNotify();
      } catch(e) {
        Cu.reportError(e);
      }
    });
  }

  timer.initWithCallback(function() {
    let resReqFile = Cc["@mozilla.org/file/local;1"].createInstance(Ci.nsIFile);
    resReqFile.initWithPath(distro.updateStampFilePath);

    if(resReqFile.exists() && resReqFile.lastModifiedTime > startupTime) {
      LOG("Update detected - requesting restart");
      notifyListeners();
    }
  }, 5000, Ci.nsITimer.TYPE_REPEATING_SLACK);

  Services.obs.addObserver(function(aSubject, aTopic, aData) {
    if (aSubject == "xpcom-will-shutdown") {
      Services.obs.removeObserver(arguments.callee, "xpcom-will-shutdown", false);
      timer.cancel();
    }
  }, "xpcom-will-shutdown", false);

  this.addListener = function URN_addListener(aListener) {
    if (!aListener) {
      throw new Error("A listener must be specified");
    }

    if ((aListener.onUpdatedNotify == undefined) ||
        (typeof(aListener.onUpdatedNotify) != "function")) {
      throw new Error("Listener must implement onUpdatedNotify");
    }

    if (listeners.indexOf(aListener) != -1) {
      throw new Error("Trying to register an observer more than once");
    }

    listeners.push(aListener);

    if (fired) {
      aListener.onUpdatedNotify();
    }
  };

  this.removeListener = function URN_removeListener(aListener) {
    let index = listeners.indexOf(aListener);
    if (index == -1) {
      throw new Error("Trying to remove an observer that was never registered");
    }

    listeners.splice(index, 1);
  };

  this.restart = function URN_restart() {
    if (!fired) {
      throw new Error("Calling restart with no pending restart request");
    }

    Cc["@mozilla.org/toolkit/app-startup;1"]
       .getService(Ci.nsIAppStartup)
       .quit(Ci.nsIAppStartup.eRestart | Ci.nsIAppStartup.eAttemptQuit);
  };
}

UpdateRestartNotifier.prototype = {
  classDescription: "Update Restart Notifier",
  classID: Components.ID("{799a4700-2085-40e8-853a-05dcf8e95e41}"),
  contractID: "@ubuntu.com/update-restart-notifier;1",
  QueryInterface: XPCOMUtils.generateQI([Ci.nsISupports])
};

const NSGetFactory = XPCOMUtils.generateNSGetFactory([UpdateRestartNotifier]);
