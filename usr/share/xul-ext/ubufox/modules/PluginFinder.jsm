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
 * Portions created by the Initial Developer are Copyright (C) 2011
 * the Initial Developer. All Rights Reserved.
 *
 * Contributor(s):
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

const Cc = Components.classes;
const Cu = Components.utils;
const Ci = Components.interfaces;

const nsITimer = Ci.nsITimer;

const INSTALL_NOT_STARTED = 0;
const INSTALL_IN_PROGRESS = 1;
const INSTALL_FINISHED = 2;

Cu.import("resource://gre/modules/Services.jsm");
Cu.import("resource://ubufox/Distro.jsm");

var EXPORTED_SYMBOLS = [ "PluginFinder", "PluginFinderDevel" ];

var install = null;

["LOG", "WARN", "ERROR"].forEach(function(aName) {
  this.__defineGetter__(aName, function() {
    Components.utils.import("resource://gre/modules/AddonLogging.jsm");

    LogManager.getLogger("ubufox.pluginfinder", this);
    return this[aName];
  });
}, this);

function safeCall() {
  let obj = arguments[0];
  let member = arguments[1];
  if (obj[member]) {
    let args = Array.prototype.splice.call(arguments, 2);
    try {
      obj[member].apply(obj, args);
    } catch(ex) { Cu.reportError(ex); }
  }
}

function installContext() {
  this.state = INSTALL_NOT_STARTED;
  this.progress = -1;
}

function installMonitor(aPid, aRequest) {
  this.pid = aPid;
  this.request = aRequest;
}

installMonitor.prototype = {
  onInstallStarted: function iM_onInstallStarted() {
    PluginFinderInternal.onInstallStarted(this.pid, this.request);
  },

  onProgressChanged: function iM_onProgressChange(aProgress) {
    PluginFinderInternal.onProgressChanged(this.pid, this.request, aProgress);
  },

  onInstallFinished: function iM_onInstallFinished() {
    PluginFinderInternal.onInstallFinished(this.pid, this.request);
  },

  onInstallFailed: function iM_onInstallFailed(aError) {
    PluginFinderInternal.onInstallFailed(this.pid, this.request, aError);
  }
};

function installRequest(aPluginInfos, aListener) {
  this.listener = aListener;
  this.installers = {};
  this.state = INSTALL_NOT_STARTED;
  this.pluginInfosLength = aPluginInfos.length;
}

function getPluginInfoRequest(aMimeType, aCallback) {
  this.mimetype = aMimeType;
  this.callback = aCallback;
  this.pendingReplies = PluginFinderInternal.providers.length;
  this.pluginInfos = [];
}

getPluginInfoRequest.prototype = {
  pluginInfoReceived: function gPIR_pluginInfoReceived(aPluginInfoArray) {
    PluginFinderInternal.pluginInfoReceived(aPluginInfoArray, this);
  },

  providerErrorReceived: function gPIR_providerErrorReceived(aError) {
    PluginFinderInternal.providerErrorReceived(aError, this);
  }
};

var PluginFinderInternal = {
  providers: [],
  installHandlers: {},

  init: function PFI_init() {
    LOG("Initializing plugin finder module");

    distro.PFSProviders.forEach(function(provider) {
      try {
        LOG("Loading provider " + provider);
        Cu.import(provider);
      } catch(e) {
        Cu.reportError("Failed to import provider: " + e);
      }
    });

    distro.PFSInstallers.forEach(function(installer) {
      try {
        LOG("Loading installer " + installer);
        Cu.import(installer);
      } catch(e) {
        Cu.reportError("Failed to import installer: " + e);
      }
    });
  },

  registerProvider: function PFI_registerProvider(aProvider) {
    if (!aProvider || typeof(aProvider.getPluginInfo) != "function") {
      throw new Error("Invalid provider");
    }

    if (this.providers.indexOf(aProvider) != -1) {
      throw new Error("Provider already registered");
    }

    this.providers.push(aProvider);
  },

  unregisterProvider: function PFI_unregisterProvider(aProvider) {
    let index = this.providers.indexOf(aProvider);
    if (index == -1) {
      throw new Error("Provider not registered");
    }

    this.providers.splice(index, 1);
  },

  registerInstallHandler: function PFI_registerInstallHandler(aHandler) {
    if (!aHandler || !aHandler.types ||
        typeof(aHandler.install) != "function") {
      throw new Error("Invalid installer");
    }

    let types = aHandler.types.split(",");
    types.forEach(function(type) {
      if (this.installHandlers[type]) {
        throw new Error("Handler already registered for type " + type);
      }
    }, this);

    types.forEach(function(type) {
      this.installHandlers[type] = aHandler;
    }, this);
  },

  unregisterInstallHandler: function PFI_unregisterInstallHandler(aHandler) {
    for (let type in this.installHandlers) {
      if (this.installHandlers[type] == aHandler) {
        delete this.installHandlers[type];
      }
    }
  },

  getPluginInfo: function PFI_getPluginInfo(aMimeType, aCallback) {
    LOG("New getPluginInfo request for " + aMimeType);
    if (typeof(aCallback) != "function") {
      throw new Error("There's no point in calling an async function \
                      without a callback");
    }

    if (!aMimeType) {
      throw new Error("No mimetype specified");
    }

    var request = new getPluginInfoRequest(aMimeType, aCallback);

    this.providers.forEach(function(provider) {
      try {
        provider.getPluginInfo(this.mimetype, this);
      } catch(ex) {
        this.pendingReplies -= 1;
        Cu.reportError(ex);
      }
    }, request);

    if (this.providers.length == 0) {
      this.doGetPluginInfoRespond(request);
    }
  },

  install: function PFI_install(aPluginInfos, aListener) {
    if (!aPluginInfos) {
      throw new Error("You forgot to specify an array of plugins");
    }

    var pluginInfos = {};

    aPluginInfos.forEach(function(pluginInfo) {
      if (pluginInfos[pluginInfo.pid]) {
        throw new Error("Duplicate plugin ID's detected");
      }

      pluginInfos[pluginInfo.pid] = pluginInfo;

      if (!this.installHandlers[pluginInfo.type]) {
        throw new Error("No handler for plugin with installation type "
                        + aPluginInfo.type);
      }
    }, this);

    var request = new installRequest(aPluginInfos, aListener);

    var timer = Cc["@mozilla.org/timer;1"].createInstance(nsITimer);
    timer.initWithCallback(function() {
      let timerKungFuDeathGrip = timer;
      aPluginInfos.forEach(function(pluginInfo) {
        this.installers[pluginInfo.pid] = new installContext();
        let mon = new installMonitor(pluginInfo.pid, this);
        try {
          PluginFinderInternal.installHandlers[pluginInfo.type].install(pluginInfo, mon);
        } catch(ex) {
          Cu.reportError("Install failed: " + ex);
          mon.onInstallFailed(null);
        }
      }, request);
    }, 0, nsITimer.TYPE_ONE_SHOT);
  },

  pluginInfoReceived: function PFI_pluginInfoReceived(aPluginInfoArray, aRequest) {
    LOG("getPluginInfo response from provider");
    if (!aPluginInfoArray) {
      throw new Error("Invalid getPluginInfo response from provider");
    }

    if (aRequest.pendingReplies <= 0) {
      ERROR("Unexpected reply from provider");
      return;
    }

    aRequest.pendingReplies -= 1;
    aRequest.pluginInfos = aRequest.pluginInfos.concat(aPluginInfoArray);
    LOG("Provider found " + aPluginInfoArray.length.toString() + " plugins");

    if (aRequest.pendingReplies == 0) {
      this.doGetPluginInfoRespond(aRequest);
    }
  },

  providerErrorReceived: function PFI_providerErrorReceived(aError, aRequest) {
    if (!aError) {
      throw new Error("Error from provider without any message");
    }

    if (aRequest.pendingReplies <= 0) {
      ERROR("Unexpected error from provider");
      return;
    }

    aRequest.pendingReplies -= 1;

    if (aRequest.pendingReplies == 0) {
      this.doGetPluginInfoRespond(aRequest);
    }
  },

  doGetPluginInfoRespond: function PFI_doGetPluginInfoRespond(aRequest) {
    var filteredPluginInfos = [];
    aRequest.pluginInfos.forEach(function(pluginInfo) {
      if (!this.installHandlers[pluginInfo.type] &&
          pluginInfo.type != "manual") {
        WARN("No install handler for " + pluginInfo.name);
      } else {
        filteredPluginInfos.push(pluginInfo);
      }
    }, this);

    LOG("Responding to getPluginInfo. Found " +
        filteredPluginInfos.length.toString() + " plugins");

    try {
      aRequest.callback(aRequest.mimetype, filteredPluginInfos);
    } catch(ex) {
      Cu.reportError(ex);
    }
  },

  onInstallStarted: function PFI_onInstallStarted(aPid, aRequest) {
    aRequest.installers[aPid].state = INSTALL_IN_PROGRESS;
    if (aRequest.state == INSTALL_NOT_STARTED) {
      aRequest.state = INSTALL_IN_PROGRESS;
      safeCall(aRequest.listener, "onInstallStarted");
    }
  },

  onProgressChanged: function PFI_onProgressChanged(aPid, aRequest, aProgress) {
    aRequest.installers[aPid].progress = aProgress;
    let progress = 0;
    for each (let installer in aRequest.installers) {
      if (installer.progress == -1) {
        continue;
      }

      progress += installer.progress / aRequest.pluginInfosLength;
      progress = Math.min(progress, 100);
      progress = Math.max(progress, 0);
    }

    safeCall(aRequest.listener, "onProgressChanged", progress);
  },

  onInstallFinished: function PFI_onInstallFinished(aPid, aRequest) {
    if (aRequest.installers[aPid].state == INSTALL_FINISHED) {
      WARN("Got onInstallFinished more than once");
      return;
    }

    this.onProgressChanged(aPid, aRequest, 100);

    aRequest.installers[aPid].state = INSTALL_FINISHED;
    safeCall(aRequest.listener, "onPluginFinished", aPid);

    for each (let installer in aRequest.installers) {
      if (installer.state != INSTALL_FINISHED) {
        return;
      }
    }

    aRequest.state = INSTALL_FINISHED;
    safeCall(aRequest.listener, "onInstallFinished");
  },

  onInstallFailed: function PFI_onInstallFailed(aPid, aRequest, aError) {
    if (aRequest.installers[aPid].state == INSTALL_FINISHED) {
      WARN("Got onInstallFinished more than once");
      return;
    }

    aRequest.installers[aPid].state = INSTALL_FINISHED;
    safeCall(aRequest.listener, "onPluginFailed", aPid, aError);

    for each (let installer in aRequest.installers) {
      if (installer.state != INSTALL_FINISHED) {
        return;
      }
    }

    aRequest.state = INSTALL_FINISHED;
    safeCall(aRequest.listener, "onInstallFinished");
  }
};

var PluginFinder = {
  registerProvider: function PF_registerProvider(aProvider) {
    PluginFinderInternal.registerProvider(aProvider);
  },

  unregisterProvider: function PF_unregisterProvider(aProvider) {
    PluginFinderInternal.unregisterProvider(aProvider);
  },

  registerInstallHandler: function PF_registerInstallHandler(aHandler) {
    PluginFinderInternal.registerInstallHandler(aHandler);
  },

  unregisterInstallHandler: function PF_unregisterInstallHandler(aHandler) {
    PluginFinderInternal.unregisterInstallHandler(aHandler);
  },

  getPluginInfo: function PF_getPluginInfo(aMimeType, aCallback) {
    PluginFinderInternal.getPluginInfo(aMimeType, aCallback);
  },

  install: function PF_install(aPluginInfos, aListener) {
    PluginFinderInternal.install(aPluginInfos, aListener);
  }
};

var PluginFinderDevel = {
  getNumberOfProviders: function PFD_getNumberOfProviders() {
    return PluginFinderInternal.providers.length;
  }
};

PluginFinderInternal.init();
