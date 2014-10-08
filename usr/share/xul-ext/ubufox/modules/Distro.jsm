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

const { utils: Cu } = Components;

Cu.import("resource://gre/modules/XPCOMUtils.jsm");
Cu.import("resource://gre/modules/Services.jsm");

var EXPORTED_SYMBOLS = [ "distro" ];

XPCOMUtils.defineLazyGetter(this, "impl", function() {
  function distroModuleImport(aResource) {
    let tmp = {};
    Cu.import(aResource, tmp);
    return tmp["DistroImpl"];
  }

  let distrib;
  try {
    distrib = Services.prefs.getCharPref("distribution.id");
  } catch(e) { };

  try {
    if (distrib == "canonical") {
      return distroModuleImport("resource://ubufox/distributions/Ubuntu.jsm");
    }
  } catch(e) {
    Cu.reportError("Failed to import distribution module: " + e);
  }

  return NullDistro;
});

var NullDistro = {
  get canReportBug() {
    return false;
  },

  reportBug: function Null_reportBug() {
    throw new Error("Don't know how to report a bug on this system");
  },

  get helpURL() {
    return null;
  },

  get PFSProviders() {
    return [];
  },

  get PFSInstallers() {
    return [];
  },

  get PFSURI() {
    return null;
  },

  get startpageURI() {
    return Services.io.newURI("about:home", null, null);
  },

  get updateStampFilePath() {
    return null;
  }
};

var distro = {
  get canReportBug() {
    let channel = "default";
    try {
      channel = Services.prefs.getCharPref("app.update.channel");
    } catch(e) { };

    return impl.canReportBug && channel != "release";
  },

  reportBug: function D_reportBug() {
    impl.reportBug();
  },

  get helpURL() {
    return impl.helpURL;
  },

  get PFSProviders() {
    return impl.PFSProviders;
  },

  get PFSInstallers() {
    return impl.PFSInstallers;
  },

  get PFSURI() {
    return impl.PFSURI;
  },

  get startpageURI() {
    return impl.startpageURI;
  },

  get updateStampFilePath() {
    return impl.updateStampFilePath;
  }
};
