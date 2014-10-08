#include <stdio.h>
#include "uarmctrl.h"
#include <time.h>
#include <unistd.h>
#include <signal.h>
#include <sys/time.h>
#include <stdlib.h>

#define DEFAULT_BASEADDR 0x43C00000U

int main()
{
	struct timespec ts;
	ts.tv_sec = 3;
	ts.tv_nsec = 0;
    UArmCtrl ctrl;
    ctrl = getUArmCtrl();
    ctrl.move(&ctrl,80,150,50,NULL);
	//printf("sleep!\n");
    nanosleep(&ts,NULL);
    ctrl.setSpeed(&ctrl,10);
    ctrl.move(&ctrl,80,-150,50,NULL);
    nanosleep(&ts,NULL);
    ctrl.move(&ctrl,80,0,50,12);
    ctrl.get(&ctrl,12);

    return 0;
}
