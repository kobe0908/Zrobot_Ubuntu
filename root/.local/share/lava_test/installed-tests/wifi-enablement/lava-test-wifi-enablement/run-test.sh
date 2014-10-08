#!/bin/bash
#
# Copyright (C) 2012, Linaro Limited.
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
#
# Author: Ricardo Salveti <rsalveti@linaro.org>
#
# TODO: Iterate and run the tests at all wifi interfaces

if [ ! -f include/sh-test-lib ]; then
    bzr branch lp:~linaro-foundations/linaro-ubuntu/sh-test-lib include
fi

source include/sh-test-lib

# check we're root
if ! check_root; then
    error_msg "Please run the test case as root"
fi

# run the tests (arguments: SSID, PSK, WPA DRIVER)
bash -x ./wifi-enablement-test.sh LAVA-WiFiTest01 LemonFileDentist nl80211
bash -x ./wifi-enablement-test.sh LAVA-WiFiTest01 LemonFileDentist wext
#bash -x ./wifi-enablement-test.sh LAVA-5GWiFiTest01 CharacterPlumSharpener nl80211
#bash -x ./wifi-enablement-test.sh LAVA-5GWiFiTest01 CharacterPlumSharpener wext
