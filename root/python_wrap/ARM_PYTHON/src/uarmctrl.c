#include "uarmctrl.h"
#include <math.h>
#include <unistd.h>
#include <sys/time.h>
#include <signal.h>
#include <time.h>
#include <signal.h>
#include <stdlib.h>

#define DIVISION(x) (int)(pow(2,(100/x - 1)))
#define DEFAULT_BASEADDR 0x43C00000U
#define CHOOSE_SPEED speed = (speed == DEFAULT)?ctrl->speed:speed;
#define FORMAT_SPEED speed = constrain(speed,0,100);
#define MIN_HEIGHT -100

double constrain(double x,double a,double b);

static void move(UArmCtrl *ctrl,double x,double y,double z,int speed);

static void rotHand(UArmCtrl *ctrl,int handrot);

static void setSpeed(UArmCtrl *ctrl,int speed);

static void get(UArmCtrl *ctrl,int speed);

static void put(UArmCtrl *ctrl,int speed);

static void movestep();

static int max_step;
static int step;
static double cx,cy,cz,xs,ys,zs;
static UArm *uarm;
timer_t timer;

static void movestep()
{
    cx += xs;
    cy += ys;
    cz += zs;
    uarm->setXYZ(uarm,cx,cy,cz,uarm->getHandrot(uarm));
    printf("cx:%f,cy:%f,cz:%f,step:%d\n",cx,cy,cz,step);
	if(step >= max_step - 1)
    {
		setitimer(ITIMER_VIRTUAL,NULL,NULL);

	}

    step ++;
}

static void movedown()
{
    cy += ys;
    uarm->setSHR(uarm,cx,cy,cz,uarm->getHandrot(uarm));
    printf("cx:%f,cy:%f,cz:%f,step:%d\n",cx,cy,cz,step);
	if(step >= max_step - 1 || uarm->ifSwitchOn(uarm) || cy <= MIN_HEIGHT)
    {
        step = max_step - 1;
		setitimer(ITIMER_VIRTUAL,NULL,NULL);

	}

    step ++;

}

static void moveup()
{
    cy += ys;
    uarm->setSHR(uarm,cx,cy,cz,uarm->getHandrot(uarm));
    printf("cx:%f,cy:%f,cz:%f,step:%d\n",cx,cy,cz,step);
	if(step >= max_step - 1)
    {
        step = max_step - 1;
		setitimer(ITIMER_VIRTUAL,NULL,NULL);

	}

    step ++;

}


static void rotHand(UArmCtrl *ctrl,int handrot)
{

}

static void setSpeed(UArmCtrl *ctrl,int speed)
{

    FORMAT_SPEED;

    ctrl->speed = speed;

}

static void get(UArmCtrl *ctrl,int speed)
{
    FORMAT_SPEED;
    CHOOSE_SPEED;

    double bs,bh,br;

    uarm->getSHR(uarm,&bs,&bh,&br);
    cx = bs;
    cy = bh;
    cz = br;
    xs = 0;
    ys = (MIN_HEIGHT - bh) / DIVISION(speed);
    zs = 0;
    max_step = DIVISION(speed);
    step = 0;


    struct itimerval tv;
    tv.it_value.tv_sec = 0;
    tv.it_value.tv_usec = 10000;
    tv.it_interval.tv_sec = 0;
    tv.it_interval.tv_usec = 10000;

    signal(SIGVTALRM,movedown);
    setitimer(ITIMER_VIRTUAL,&tv,NULL);

    while(step < max_step);

    uarm->pumpOn(uarm);

    step = 0;
    ys = -ys;

    signal(SIGVTALRM,moveup);
    setitimer(ITIMER_VIRTUAL,&tv,NULL);

    while(step < max_step);




}

static void put(UArmCtrl *ctrl,int speed)
{
    FORMAT_SPEED;
    CHOOSE_SPEED;

    double bs,bh,br;

    uarm->getSHR(uarm,&bs,&bh,&br);
    cx = bs;
    cy = bh;
    cz = br;
    xs = 0;
    ys = (MIN_HEIGHT - bh) / DIVISION(speed);
    zs = 0;
    max_step = DIVISION(speed);
    step = 0;


    struct itimerval tv;
    tv.it_value.tv_sec = 0;
    tv.it_value.tv_usec = 10000;
    tv.it_interval.tv_sec = 0;
    tv.it_interval.tv_usec = 10000;

    signal(SIGVTALRM,movedown);
    setitimer(ITIMER_VIRTUAL,&tv,NULL);

    while(step < max_step);

    uarm->pumpOff(uarm);

    step = 0;
    ys = -ys;

    signal(SIGVTALRM,moveup);
    setitimer(ITIMER_VIRTUAL,&tv,NULL);

    while(step < max_step);


}

static void move(UArmCtrl *ctrl,double x,double y,double z,int speed)
{
    FORMAT_SPEED;
    CHOOSE_SPEED;
    uarm = &ctrl->uarm;
    double bx,by,bz;    //base xyz

    uarm->getXYZ(uarm,&bx,&by,&bz);
	printf("bx:%f,by:%f,bz:%f\n",bx,by,bz);
    cx = bx;
    cy = by;
    cz = bz;
    xs = (x - bx) / DIVISION(speed);
    ys = (y - by) / DIVISION(speed);
    zs = (z - bz) / DIVISION(speed);
    max_step = DIVISION(speed);
    step = 0;

    /*struct sigevent evp;
    struct itimerspec ts;

    int ret;

    evp.sigev_value.sival_ptr = &timer;
    evp.sigev_notify = SIGEV_SIGNAL;
    evp.sigev_signo = SIGUSR1;
    signal(SIGUSR1, movestep);

    ret = timer_create(CLOCK_REALTIME, &evp, &timer);
    if( ret )
        perror("timer_create");

    ts.it_interval.tv_sec = 0;
    ts.it_interval.tv_nsec = 10000000;
    ts.it_value.tv_sec = 0;
    ts.it_value.tv_nsec = 10000000;

    ret = timer_settime(timer, 0, &ts, NULL);
*/
    struct itimerval tv;
    tv.it_value.tv_sec = 0;
    tv.it_value.tv_usec = 10000;
    tv.it_interval.tv_sec = 0;
    tv.it_interval.tv_usec = 10000;

    signal(SIGVTALRM,movestep);
    setitimer(ITIMER_VIRTUAL,&tv,NULL);

    while(step < max_step);
	//printf("!!!!!!!!!!!!!!!!!!!\n");
}


UArmCtrl getUArmCtrl()
{
    UArmCtrl ctrl;
    ctrl.speed = 100;
    ctrl.uarm = getUArm(0x43C00000U);
    ctrl.setSpeed = setSpeed;
    ctrl.get = get;
    ctrl.put = put;
    ctrl.move = move;
    return ctrl;
}
