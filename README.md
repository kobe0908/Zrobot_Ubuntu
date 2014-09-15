Zrobot_Ubuntu
=============
Zrobot Ubuntu use Ubuntu 12.04 for ARM.

Module Drivers:
===============
These driver ko file needs to recompile if you change kernel or its config.

1.360 Wifi support
/etc/Wireless/RT2870STA/mt7601Usta.ko

2.PWM support
/root/package_c/pwmdriver.ko
/root/pwm_close_loop_app/pwmdriver.ko
/root/pwm_open_loop_app/pwmdriver.ko (not use)

3.Optical Support
/root/package_c/optical.ko
/root/optical_app/optical.ko

4.Ultrasonic Support
/root/package_c/ultrasonic.ko
/root/ultrasonic_app/ultrasonic.ko

Notice:
=======
You can visit http://www.ubuntu.com/ for supports
License:Creative Commons ShareAlike 3.0 License (CC-BY-SA)
http://creativecommons.org/licenses/by-sa/3.0/
