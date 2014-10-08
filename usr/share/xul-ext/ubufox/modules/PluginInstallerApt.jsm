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
const nsILocalFile = Ci.nsILocalFile;
const nsIProcess = Ci.nsIProcess;
const nsIFileURL = Ci.nsIFileURL;

const APTD_DBUS_NAME = "org.debian.apt";
const APTD_DBUS_IFACE = "org.debian.apt";
const APTD_DBUS_TRANSACTION_IFACE = "org.debian.apt.transaction";

var EXPORTED_SYMBOLS = [ ];

Cu.import("resource://ubufox/PluginFinder.jsm");
Cu.import("resource://ubufox/libs/gio.jsm");
Cu.import("resource://ubufox/libs/gobject.jsm");
Cu.import("resource://ubufox/libs/glib.jsm");
Cu.import("resource://gre/modules/Services.jsm");
Cu.import("resource://gre/modules/ctypes.jsm");
Cu.import("resource://gre/modules/AddonManager.jsm");

["LOG", "WARN", "ERROR"].forEach(function(aName) {
  this.__defineGetter__(aName, function() {
    Components.utils.import("resource://gre/modules/AddonLogging.jsm");

    LogManager.getLogger("ubufox.plugininstaller.apt", this);
    return this[aName];
  });
}, this);

const ERROR_MSGS = {
  "error-package-download-failed": "plugininstaller.apt.error.download_failed",
  "error-dep-resolution-failed": "plugininstaller.apt.error.dependencies",
  "error-no-lock": "plugininstaller.apt.error.lock",
  "error-no-package": "plugininstaller.apt.error.does_not_exist",
  "error-package-already-installed": "plugininstaller.apt.error.already_installed",
  "error-package-manager-failed": "plugininstaller.apt.error.failed_install",
  "error-cache-broken": "plugininstaller.apt.error.broken_cache",
  "error-package-unauthenticated": "plugininstaller.apt.error.unauthenticated",
  "error-incomplete-install": "plugininstaller.apt.error.incomplete_install",
  "error-unreadable-package-file": "plugininstaller.apt.error.open_failed",
  "error-invalid-package-file": "plugininstaller.apt.error.policy_violation"
};

var gAptPluginInstaller = null;

function AptInstallContext(aListener, aPkgName, aComp) {
  this.listener = aListener;
  this.pkgname = aPkgName;
  this.comp = aComp;
}

var PluginInstallerAptFallback = {
  init: function PIAF_init() {
    let file = Cc["@mozilla.org/file/local;1"].createInstance(nsILocalFile);
    file.initWithPath("/usr/bin/apturl");
    if (file.isExecutable()) {
      gAptPluginInstaller = PluginInstallerAptFallback;
      PluginFinder.registerInstallHandler(PluginInstallerIface);
      LOG("Using apturl fallback for apt installer");
    } else {
      WARN("No apt installer available");
    }
  },

  install: function PIAF_install(aPluginInfo, aListener) {
    let apturl = Cc["@mozilla.org/file/local;1"].createInstance(nsILocalFile);
    apturl.initWithPath("/usr/bin/apturl");

    let proc = Cc["@mozilla.org/process/util;1"].createInstance(nsIProcess);
    proc.init(apturl);

    let proxyType = -1;
    let proxyHost = "";
    let proxyPort = -1;
    try {
      proxyType = Services.prefs.getIntPref("network.proxy.type");
      proxyHost = Services.prefs.getCharPref("network.proxy.http");
      proxyPort = Services.prefs.getIntPref("network.proxy.http_port");
    } catch(ex) {};

    let httpProxy = "";
    if (proxyType > 0 && proxyHost != "") {
      httpProxy = proxyHost;
      if (proxyPort > 0) {
        httpProxy = httpProxy + ":" + proxyPort;
      }
    }

    let args = [];
    if (httpProxy != "") {
      args.push("--http-proxy");
      args.push(httpProxy);
    }
    args.push(aPluginInfo.location);

    try {
      proc.runAsync(args, args.length, {
        observe: function(aSubject, aTopic, aData) {
          if (aTopic == "process-failed") {
            Cu.reportError("Failed to run child process");
            aListener.onInstallFailed(PluginInstallerAptFallback
                                      .getString("plugininstaller.apt.error.child_process"));
          } else if (aTopic == "process-finished") {
            switch (aSubject.QueryInterface(nsIProcess).exitValue) {
            case 0:
              aListener.onInstallFinished();
              break;

            default:
              aListener.onInstallFailed(PluginInstallerAptFallback
                                        .getString("plugininstaller.apt.error.unexpected"));
              break;
            }
          }
        }
      }, false);
      aListener.onInstallStarted();
    } catch(ex) {
      Cu.reportError("Failed to execute child process: " + ex);
      aListener.onInstallFailed(this.getString("plugininstaller.apt.error.child_process"));
    }
  },

  getString: function PIAF_getString(aName) {
    if (!this._strbundle) {
      this._strbundle =
        Services.strings.createBundle("chrome://ubufox/locale/plugins.properties");
    }

    return this._strbundle.GetStringFromName(aName);
  }
};

var PluginInstallerApt = {
  _pendingComponentChecks: [],
  _pendingInstalls: [],
  _sourcesChanged: false,

  init: function PIA_init() {
    try {
      if (Services.prefs.getBoolPref("extensions.ubufox.plugin-finder.use-apturl")) {
        LOG("Preferring apturl");
        PluginInstallerAptFallback.init();
        return;
      }
    } catch(ex) { };

    if (!gio.g_dbus_proxy_new_for_bus) {
      LOG("No GDBus. Falling back to apturl");
      PluginInstallerAptFallback.init();
      return;
    }

    this.newProxyForBus(gio.G_BUS_TYPE_SYSTEM, APTD_DBUS_NAME,
                        "/org/debian/apt", APTD_DBUS_IFACE, function(aProxy,
                                                                     aError) {
      if (!aError.isNull()) {
        LOG("Failed to get proxy for aptdaemon: " +
            aError.contents.message.readString());
        PluginInstallerAptFallback.init();
        return;
      }

      let owner = gio.g_dbus_proxy_get_name_owner(aProxy);
      if (owner.isNull()) {
        LOG("Aptdaemon is not available");
        PluginInstallerAptFallback.init();
        return;
      }

      glib.g_free(owner);

      gAptPluginInstaller = PluginInstallerApt;
      PluginFinder.registerInstallHandler(PluginInstallerIface);
      LOG("Using aptdaemon for apt installer");
    });
  },

  install: function PIA_install(aPluginInfo, aListener) {
    let uri = Services.io.newURI(aPluginInfo.location, null, null);
    let re = /([^\?]*)\??(.*)/;
    let pkgname = uri.path.replace(re, "$1");
    let params = uri.path.replace(re, "$2").split('&');

    re = /([^=]*)=?(.*)/;
    var comp = null;
    params.forEach(function(param) {
      if (param.replace(re, "$1") == "section") {
        comp = param.replace(re, "$2");
      }
    });

    LOG("Starting apt install for " + pkgname + " from component " + comp);

    var ctxt = new AptInstallContext(aListener, pkgname, comp);

    if (!comp) {
      this.startInstall(ctxt);
      return;
    }

    this._pendingInstalls.push(ctxt);

    if (this._pendingComponentChecks.indexOf(comp) == -1) {
      this._pendingComponentChecks.push(comp);
      AddonManager.getAddonByID("ubufox@ubuntu.com", function(aAddon) {
        let python = Cc["@mozilla.org/file/local;1"].createInstance(nsILocalFile);
        python.initWithPath("/usr/bin/python");

        let proc = Cc["@mozilla.org/process/util;1"].createInstance(nsIProcess);
        proc.init(python);

        let args = [];
        args.push(aAddon.getResourceURI("scripts/check-component-enabled.py")
                        .QueryInterface(nsIFileURL).file.path);
        args.push(comp);

        proc.runAsync(args, args.length, {
          observe: function(aSubject, aTopic, aData) {
            if (aTopic == "process-failed") {
              Cu.reportError("Failed to check if component " + comp + " is " +
                             "enabled. Failed to run helper");
              PluginInstallerApt.startPendingForComponent(comp);
            } else if (aTopic == "process-finished") {
              switch(aSubject.QueryInterface(nsIProcess).exitValue) {
              case 0:
                PluginInstallerApt.startPendingForComponent(comp);
                break;

              case 1:
                PluginInstallerApt.maybeEnableComponent(comp);
                break;

              default:
                Cu.reportError("Failed to check if component " + comp + " is " +
                               "enabled. Helper returned with exit code " +
                               aSubject.QueryInterface(nsIProcess).exitValue.toString());
                // We don't know if the required component is enabled, but try
                // the install anyway
                PluginInstallerApt.startPendingForComponent(comp);
                break;
              }
            }
          }
        }, false);
      });
    }
  },

  startPendingForComponent: function PIA_startPendingForComponent(aComp) {
    LOG("Starting pending installs for component " + aComp);

    this._pendingComponentChecks.splice(aComp);

    var starting = [];
    this._pendingInstalls.forEach(function(aCtxt) {
      if (aCtxt.comp == aComp) {
        starting.push(aCtxt);
      }
    });

    starting.forEach(function(aCtxt) {
      this.startInstall(aCtxt);
      this._pendingInstalls.splice(this._pendingInstalls.indexOf(aCtxt));
    }, this);

    this.maybeUpdateCacheAndStartPending(false);
  },

  failPendingForComponent: function PIA_failPendingForComponent(aComp, aError) {
    Cu.reportError("Cancelling installs for component " + aComp + ": " + aError);

    this._pendingComponentChecks.splice(aComp);

    var failed = [];
    this._pendingInstalls.forEach(function(aCtxt) {
      if (aCtxt.comp == aComp) {
        failed.push(aCtxt);
      }
    });

    failed.forEach(function(aCtxt) {
      aCtxt.listener.onInstallFailed(aError);
      this._pendingInstalls.splice(this._pendingInstalls.indexOf(aCtxt));
    }, this);

    this.maybeUpdateCacheAndStartPending(false);
  },

  maybeEnableComponent: function PIA_maybeEnableComponent(aComp) {
    let count;
    this._pendingInstalls.forEach(function(aCtxt) {
      if (aCtxt.comp == aComp) {
        count += 1;
      }
    });

    let title;
    if (count <= 1) {
      title = "plugininstaller.apt.enable-source-dialog.title.single";
    } else {
      title = "plugininstaller.apt.enable-source-dialog.title.multiple";
    }

    if (Services.prompt.confirm(null, this.getString(title),
                                this.getFormatString("plugininstaller.apt.enable-source-dialog.body",
                                                     [aComp]))) {
      this.enableComponent(aComp);
    } else {
      this.failPendingForComponent(aComp, this.getString("plugininstaller.apt.error.component-not-enabled"));
    }
  },

  enableComponent: function PIA_enableComponent(aComp) {
    LOG("Enabling source component " + aComp);
    PluginInstallerApt.createAndRunTransaction("EnableDistroComponent",
                                               glib.g_variant_new("(s)",
                                                                  ctypes.char.array()(aComp).address()),
                                               {
      onTransactionFailed: function(aError) {
        Cu.reportError("Failed to enable component " + aComp + ": " +
                       aError.contents.message.readString());
        PluginInstallerApt.failPendingForComponent
          (aComp, PluginInstallerApt.getString("plugininstaller.apt.error.component-not-enabled"));
      },

      onTransactionFinished: function(aExitState, aErrorCode, aErrorDetails) {
        if (aExitState != "exit-success") {
          Cu.reportError("Failed to enable component " + aComp);
          PluginInstallerApt.failPendingForComponent
            (aComp, PluginInstallerApt.getString("plugininstaller.apt.error.component-not-enabled"));
        } else {
          LOG("Enabled component " + aComp);
          PluginInstallerApt._pendingComponentChecks.splice(aComp);
          PluginInstallerApt.maybeUpdateCacheAndStartPending(true);
        }
      }
    });
  },

  maybeUpdateCacheAndStartPending: function PIA_maybeUpdateCacheAndStartPending(aChanged) {
    if (aChanged) {
      LOG("Marking sources as changed");
      this._sourcesChanged = true;
    }

    if (this._pendingComponentChecks.length != 0) {
      return;
    }

    if (!this._sourcesChanged) {
      LOG("Not updating cache, as no sources have changed");
      return;
    }

    this._sourcesChanged = false;

    this.updateCache(function() {
      var startList = [];
      PluginInstallerApt._pendingInstalls.forEach(function(aCtxt) {
        startList.push(aCtxt);
      });

      startList.forEach(function(aCtxt) {
        PluginInstallerApt.startInstall(aCtxt);
        PluginInstallerApt._pendingInstalls.splice(aCtxt);
      });
    });
  },

  updateCache: function PIA_updateCache(aCallback) {
    LOG("Updating cache");
    PluginInstallerApt.createAndRunTransaction("UpdateCache", null, {
      onTransactionFailed: function(aError) {
        Cu.reportError("Failed to update cache: " +
                       aError.contents.message.readString());
        aCallback();
      },

      onTransactionFinished: function(aExitState, aErrorCode, aErrorDetails) {
        if (aExitState != "exit-success") {
          Cu.reportError("Error whilst updating cache");
        } else {
          LOG("Successfully updated cache");
        }

        aCallback();
      }
    });
  },

  startInstall: function PIA_startInstall(aCtxt) {
    let builder = new glib.GVariantBuilder;
    glib.g_variant_builder_init(builder.address(), "a*");
    glib.g_variant_builder_add(builder.address(), "s",
                               ctypes.char.array()(aCtxt.pkgname).address());
    let inner = glib.g_variant_builder_end(builder.address());
    glib.g_variant_builder_clear(builder.address());

    glib.g_variant_builder_init(builder.address(), "r");
    glib.g_variant_builder_add_value(builder.address(), inner);
    let params = glib.g_variant_builder_end(builder.address());
    glib.g_variant_builder_clear(builder.address());

    PluginInstallerApt.createAndRunTransaction("InstallPackages", params, {
      onTransactionFailed: function(aError) {
        Cu.reportError("Error installing " + aCtxt.pkgname + ": " +
                       aError.contents.message.readString() + " (domain: " +
                       aError.contents.domain + ", code: " +
                       aError.contents.code + ")");
        let msg = null;
        if (aError.contents.domain == gio.G_IO_ERROR &&
            aError.contents.code == gio.G_IO_ERROR_DBUS_ERROR) {
          let rerr = gio.g_dbus_error_get_remote_error(aError).readString();
          if (rerr == "org.freedesktop.PolicyKit.Error.NotAuthorized") {
            msg = PluginInstallerApt.getString("plugininstaller.apt.error.unauthorized");
          }
        }

        if (!msg) {
          msg = PluginInstallerApt.getString("plugininstaller.apt.error.unexpected");
        }

        aCtxt.listener.onInstallFailed(msg);
      },

      onTransactionFinished: function(aExitState, aErrorCode, aErrorDetails) {
        if (aExitState != "exit-success") {
          aCtxt.listener.onInstallFailed(PluginInstallerApt.getErrorMessage(aErrorCode));
        } else {
          aCtxt.listener.onInstallFinished();
        }
      },

      onTransactionProgressChanged: function(aProgress) {
        aCtxt.listener.onProgressChanged(aProgress)
      },

      onTransactionStarted: function() {
        aCtxt.listener.onInstallStarted();
      }
    });
  },

  createAndRunTransaction: function PIA_createAndRunTransaction(aRole, aParams,
                                                                aObserver) {
    LOG("Creating " + aRole + " transaction");
    this.newProxyForBus(gio.G_BUS_TYPE_SYSTEM, APTD_DBUS_NAME, "/org/debian/apt",
                        APTD_DBUS_IFACE, function(aProxy, aError) {
      if (!aError.isNull()) {
        Cu.reportError("Failed to get GDBusProxy for aptdaemon: " +
                       aError.contents.message.readString());
        if (aObserver.onTransactionFailed) {
          aObserver.onTransactionFailed(aError);
        }
        return;
      }

      PluginInstallerApt.proxyCall(aProxy, aRole, aParams, function(aResult,
                                                                    aError) {
        if (!aError.isNull()) {
          Cu.reportError(aRole + "() method failed: " +
                         aError.contents.message.readString());
          if (aObserver.onTransactionFailed) {
            aObserver.onTransactionFailed(aError);
          }
          return;
        }

        let path = new ctypes.char.ptr;
        glib.g_variant_get(aResult, "(s)", path.address());

        PluginInstallerApt.newProxyForBus(gio.G_BUS_TYPE_SYSTEM, APTD_DBUS_NAME,
                                          path.readString(),
                                          APTD_DBUS_TRANSACTION_IFACE,
                                          function(aProxy, aError) {
          if (!aError.isNull()) {
            Cu.reportError("Failed to get transaction proxy for " + aRole +
                           ": " + aError.contents.message.readString());
            if (aObserver.onTransactionFailed) {
              aObserver.onTransactionFailed(aError);
            }
            return;
          }

          gobject.g_object_ref(aProxy);

          var name = gio.g_dbus_proxy_get_name(aProxy).readString();
          var iface = gio.g_dbus_proxy_get_interface_name(aProxy).readString();
          var path = gio.g_dbus_proxy_get_object_path(aProxy).readString();

          var running = false;
          var errorCode = new ctypes.char.ptr;
          var errorDetails = new ctypes.char.ptr;

          var id = gobject.GSignalConnect(aProxy, "g-signal", function(aProxy,
                                                                       aSender,
                                                                       aSignal,
                                                                       aParams,
                                                                       aData) {
            let signal = aSignal.readString();
            LOG("Got signal " + iface + "." + signal + "()" + " from " + path +
                " on " + name);
            if (signal == "PropertyChanged") {
              let namePtr = new ctypes.char.ptr;
              let variant = new glib.GVariant.ptr;
              glib.g_variant_get(aParams, "(sv)", namePtr.address(),
                                 variant.address());

              // FIXME: Desperately need some sanity checking in here

              let name = namePtr.readString();
              LOG("Property - " + name);

              if (name == "Progress") {
                if (!running) {
                  return;
                }

                let progress = glib.g_variant_get_int32(variant);
                LOG("Progress = " + progress.toString());
                if (aObserver.onTransactionProgressChanged) {
                  aObserver.onTransactionProgressChanged(progress);
                }

              } else if (name == "ExitState") {
                let exitState = glib.g_variant_get_string(variant, null).readString();
                LOG("ExitState = " + exitState);
                if (aObserver.onTransactionFinished) {
                  aObserver.onTransactionFinished(exitState, errorCode, errorDetails);
                }
                gobject.GSignalHandlerDisconnect(aProxy, id);
                gobject.g_object_unref(aProxy);

              } else if (name == "Status") {
                let status = glib.g_variant_get_string(variant, null).readString();
                LOG("Status = " + status);
                if (status == "status-running" && !running) {
                  running = true;
                  if (aObserver.onTransactionStarted) {
                    aObserver.onTransactionStarted();
                  }
                }

              } else if (name == "Error") {
                glib.g_variant_get(variant, "(ss)", errorCode.address(),
                                   errorDetails.address());
                Cu.reportError("Error: " + errorCode.readString() + " (" +
                               errorDetails.readString() + ")");
              }
            }
          }, ctypes.void_t, [gio.GDBusProxy.ptr, glib.gchar.ptr, glib.gchar.ptr,
                             glib.GVariant.ptr, glib.gpointer]);

          PluginInstallerApt.proxyCall(aProxy, "Run", null, function(aResult,
                                                                     aError) {
            if (!aError.isNull()) {
              Cu.reportError("Failed to run transaction: " + 
                             aError.contents.message.readString());
              gobject.GSignalHandlerDisconnect(aProxy, id);
              gobject.g_object_unref(aProxy);
              if (aObserver.onTransactionFailed) {
                aObserver.onTransactionFailed(aError);
              }
            }
          });
        });
      });
    });
  },

  newProxyForBus: function PIA_newProxyForBus(aBus, aName, aPath, aIface,
                                              aCallback) {
    LOG("Creating proxy for iface=" + aIface + ", path=" + aPath + " on " + aName);
    gio.GDbusProxyNewForBus(aBus, gio.G_DBUS_PROXY_FLAGS_NONE, null,
                            aName, aPath, aIface, null, function(aObject,
                                                                 aResult) {
      let error = new glib.GError.ptr;
      let proxy = gio.g_dbus_proxy_new_for_bus_finish(aResult, error.address());
      try {
        aCallback(proxy, error);
      } finally {
        if (!error.isNull()) {
          glib.g_error_free(error);
        }
        if (!proxy.isNull()) {
          gobject.g_object_unref(proxy);
        }
      }
    });
  },

  proxyCall: function PIA_proxyCall(aProxy, aMethod, aParams, aCallback) {
    var name = gio.g_dbus_proxy_get_name(aProxy);
    var iface = gio.g_dbus_proxy_get_interface_name(aProxy);
    var path = gio.g_dbus_proxy_get_object_path(aProxy);
    LOG("Calling " + iface.readString() + "." + aMethod + "() on " +
        path.readString() + "," + name.readString());

    gio.GDbusProxyCall(aProxy, aMethod, aParams, gio.G_DBUS_CALL_FLAGS_NONE,
                       -1, null, function(aObject, aResult) {
      let error = new glib.GError.ptr;
      let res = gio.g_dbus_proxy_call_finish(ctypes.cast(aObject, gio.GDBusProxy.ptr),
                                             aResult, error.address());
      try {
        aCallback(res, error);
      } finally {
        if (!error.isNull()) {
          glib.g_error_free(error);
        }
        if (!res.isNull()) {
          glib.g_variant_unref(res);
        }
      }
    });
  },

  getErrorMessage: function PIA_getErrorMessage(aErrorCode) {
    let err_code = aErrorCode.readString();
    if (err_code in ERROR_MSGS) {
      return this.getString(ERROR_MSGS[err_code]);
    } else {
      return this.getString("plugininstaller.apt.error.unexpected");
    }
  },

  getFormatString: function PIA_getFormatString(aName, aParams) {
    if (!this._strbundle) {
      this._strbundle =
        Services.strings.createBundle("chrome://ubufox/locale/plugins.properties");
    }

    return this._strbundle.formatStringFromName(aName, aParams, aParams.length);
  },

  getString: function PIA_getString(aName) {
    if (!this._strbundle) {
      this._strbundle =
        Services.strings.createBundle("chrome://ubufox/locale/plugins.properties");
    }

    return this._strbundle.GetStringFromName(aName);
  }
};

var PluginInstallerIface = {
  types: "apt",

  install: function PII_install(aPluginInfo, aListener) {
    gAptPluginInstaller.install(aPluginInfo, aListener);
  }
};

PluginInstallerApt.init();
