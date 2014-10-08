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

const { classes: Cc, interfaces: Ci, utils: Cu } = Components;

Cu.import("resource://gre/modules/Services.jsm");
Cu.import("resource://gre/modules/XPCOMUtils.jsm");
Cu.import("resource://gre/modules/FileUtils.jsm");

var EXPORTED_SYMBOLS = [ "DistroImpl" ];

const HOMEPAGE_GOOGLE_QUERY = "sourceid=hp";

function apportExists() {
  try {
    let executable = new FileUtils.File("/usr/bin/ubuntu-bug");
    return executable.isExecutable();
  } catch(e) {
    return false;
  }
}

function getCurrentSearchEngineParams() {
  try {
    if (Services.search.currentEngine.searchForm.indexOf("search.yahoo.com")
        != -1) {
      return {"name": "Yahoo", "query": null};
    } else {
      return {"name": "Google", "query": HOMEPAGE_GOOGLE_QUERY};
    }
  } catch(e) { return {"name": "Google", "query": HOMEPAGE_GOOGLE_QUERY}; }
}

var DistroImpl = {
  get canReportBug() {
    return apportExists()
  },

  reportBug: function Ubuntu_reportBug() {
    if (!apportExists()) {
      throw new Error("Apport must be installed in order to report a bug");
    }

    let executable = new FileUtils.File("/usr/bin/ubuntu-bug");

    let procUtil = Cc["@mozilla.org/process/util;1"].createInstance(Ci.nsIProcess);
    procUtil.init(executable);

    let pkgname = Cc["@mozilla.org/xre/app-info;1"]
                  .getService(Ci.nsIXULAppInfo).name.toLowerCase()
    if (!pkgname) {
        pkgname = "firefox";
    }
    let args = new Array(pkgname);

    procUtil.run(false, args, args.length);
  },

  get helpURL() {
    return "https://launchpad.net/distros/ubuntu/" + VersionInfo.codename + "/+sources/firefox/+gethelp";
  },

  get PFSProviders() {
    return [ "resource://ubufox/PluginProviderPFS.jsm" ];
  },

  get PFSInstallers() {
    return [
      "resource://ubufox/PluginInstallerApt.jsm",
      "resource://ubufox/PluginInstallerExternal.jsm"
    ]
  },

  get PFSURI() {
    return "https://mozilla-pfs.ubuntu.com/plugin-finder?mimetype=%PLUGIN_MIMETYPE%&appID=%APP_ID%&appVersion=%APP_VERSION%&clientOS=%CLIENT_OS%&chromeLocale=%CHROME_LOCALE%&distributionID=" + VersionInfo.version.replace(/^([^\.]*)\.([^\.]*).*/, "$1.$2");
  },

  get startpageURI() {
    let params = getCurrentSearchEngineParams();
    let baseuri = Services.io.newURI("http://start.ubuntu.com/", null, null);
    let spec = "";
    if (VersionInfo.version) {
      spec += VersionInfo.version.replace(/^([^\.]*)\.([^\.]*).*/,
                                          "$1.$2") + "/";
    }
    spec += params.name + "/";
    if (params.query != null) {
      spec += "?" + params.query;
    }

    return Services.io.newURI(spec, null, baseuri);
  }
};

XPCOMUtils.defineLazyGetter(DistroImpl, "updateStampFilePath", function() {
  let major = Number(VersionInfo.version.replace(/^([0-9]*)\.([0-9]*).*/, "$1"));
  let minor = Number(VersionInfo.version.replace(/^([0-9]*)\.([0-9]*).*/, "$2"));
  if (major < 10 || (major == 10 && minor == 4)) {
    return "/var/lib/update-notifier/user.d/" +
           Services.appinfo.name.toLowerCase() + "-restart-required";
  } else {
    return "/var/run/" + Services.appinfo.name.toLowerCase() +
           "-restart-required";
  }
});

XPCOMUtils.defineLazyGetter(this, "VersionInfo", function() {
  const PROPERTIES = {
    "DISTRIB_RELEASE": "version",
    "DISTRIB_CODENAME": "codename"
  };

  let res = new Object();

  try {
    let istream = Services.io.newChannel("file:///etc/lsb-release",
                                         null, null).open();
    let re = /^([^=]*)=?(.*)/;

    // It sucks that we need to do synchronous IO here, but we may be
    // called from the startpage nsIAboutModule.newChannel, and can't do
    // anything async there
    line = { value: "" };
    while (istream.readLine(line)) {
      let key = line.value.replace(re, "$1");
      let value = line.value.replace(re, "$2");
      if (key in PROPERTIES) {
        res[PROPERTIES[key]] = value;
      }
    }
  } catch(e) {
    Cu.reportError("Failed to read lsb-release: " + e);
  }

  return res;
});
