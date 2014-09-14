#include <stdio.h>
#include <fcntl.h>
#include <unistd.h>
#include <string.h>
#include <sys/time.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <syslog.h>
#include <memory.h>

#include "motor.h"
#include "eye.h"
#include "xil_io.h"

#define FRONT 0
#define BACK 1

#define MODE (O_WRONLY | O_TRUNC)

#define AXI_GPIO_BASEADDR 0x41200000
#define AXI_PWM_BASEADDR  0x43C01000

#define SPEED_OFFSET 2000
static char *gpio_addr[] = {
	"/sys/class/gpio/export",
	"/sys/class/gpio/gpio61/direction/","/sys/class/gpio/gpio61/value/",
	"/sys/class/gpio/gpio62/direction/","/sys/class/gpio/gpio62/value/",
	"/sys/class/gpio/gpio63/direction/","/sys/class/gpio/gpio63/value/",
	"/sys/class/gpio/gpio64/direction/","/sys/class/gpio/gpio64/value/"
};

static int fd;
struct CAR_STATE state;
void car_init()
{
	state.ldir=0;
	state.lspd=0;
	state.rdir=0;
	state.rspd=0;
	car_set();
}

void car_set()
{
	left_wheel(state.ldir,state.lspd);
	right_wheel(state.rdir,state.rspd);
}

void left_wheel(int dir,int spd)
{
	Xil_Out32(AXI_PWM_BASEADDR + 4, dir);
	Xil_Out32(AXI_PWM_BASEADDR,      spd == 0 ? 0 : 0x80000000 | spd);
}
void right_wheel(int dir,int spd)
{
	Xil_Out32(AXI_PWM_BASEADDR + 12, dir);
	Xil_Out32(AXI_PWM_BASEADDR + 8,  spd == 0 ? 0 : 0x80000000 | spd);
}
void move(enum ACTION act,int spd)
{
	switch(act)
	{
		case FORW:
			state.ldir=FRONT;
			state.rdir=FRONT;
			state.lspd=spd;
			state.rspd=spd;
			break;
		case BACK:
			state.ldir=BACK;
			state.rdir=BACK;
			state.lspd=spd;
			state.rspd=spd;
			break;
		case LEFT:
			state.ldir=BACK;
			state.rdir=FRONT;
			state.lspd=spd;
			state.rspd=spd;
			break;
		case RIGHT:
			state.ldir=FRONT;
			state.rdir=BACK;
			state.lspd=spd;
			state.rspd=spd;
			break;
	}
	car_set();
}

void stop()
{
	left_wheel(FRONT,0);
	right_wheel(FRONT,0);
}
