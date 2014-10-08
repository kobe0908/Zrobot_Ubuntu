#include <stdio.h>
#include <unistd.h>
#include "xil_io.h"
#include "uarm.h"


#define DEFAULT_BASEADDR 0x43C00000U
#define SPEED_MAX 100.0
#define SLEEP_MAX_US 10000

#define ADDR(x) (uarm->attr.base_address + 4 * x)




static void setPosXYZ(UArm *uarm,PosXYZ xyz);
static void pumpOn(UArm *uarm);
static void pumpOff(UArm *uarm);
static void init(UArm *uarm,unsigned int addr);
static void setSHR(UArm *uarm,double stretch,double height,int rot,int handrot);
static void setXYZ(UArm *uarm,double x,double y,double z,int handrot);
static void XYtoSR(PosXYZ xyz,PosSHR *shr);
static void SRtoXY(PosSHR shr,PosXYZ *xyz);
static void setPosXYZ(UArm *uarm,PosXYZ xyz);
static void formatSHR(PosSHR *shr);
static void setPosSHR(UArm *uarm,PosSHR shr);
static void setServo(UArm *uarm,char channel,int angle);
static char ifSwitchOn(UArm *uarm);
static PosSHR getPosSHR(UArm *uarm);
static PosXYZ getPosXYZ(UArm *uarm);
static void getXYZ(UArm *uarm,double *x,double *y,double *z);
static void getSHR(UArm *uarm,double *s,double *h,double *r);
static int getHandrot(UArm *uarm);

static int getHandrot(UArm *uarm)
{
    return uarm->status.pos.handrot;

}

static void getSHR(UArm *uarm,double *s,double *h,double *r)
{
    *s = uarm->status.pos.s;
    *h = uarm->status.pos.h;
    *r = uarm->status.pos.r;
}

static void getXYZ(UArm *uarm,double *x,double *y,double *z)
{
    PosXYZ xyz = uarm->getPosXYZ(uarm);
    *x = xyz.x;
    *y = xyz.y;
    *z = xyz.z;
}


static PosSHR getPosSHR(UArm *uarm)
{
    return uarm->status.pos;
}

static PosXYZ getPosXYZ(UArm *uarm)
{
    PosXYZ xyz;
    SRtoXY(uarm->status.pos,&xyz);
    return xyz;

}



UArm getUArm(unsigned int addr)
{
    UArm uarm;
    uarm.setPosSHR = setPosSHR;
    uarm.setPosXYZ = setPosXYZ;
    uarm.setSHR = setSHR;
    uarm.setXYZ = setXYZ;
    uarm.ifSwitchOn = ifSwitchOn;
    uarm.pumpOn = pumpOn;
    uarm.pumpOff = pumpOff;
    uarm.init = init;
    uarm.getPosSHR = getPosSHR;
    uarm.getPosXYZ = getPosXYZ;
    uarm.getSHR = getSHR;
    uarm.getXYZ = getXYZ;
    uarm.getHandrot = getHandrot;

    uarm.init(&uarm,addr);

    return uarm;

}

double constrain(double x,double a,double b)
{
	double temp_min,temp_max;
    temp_min = (a < b) ? a : b;
    temp_max = (a > b) ? a : b;
    if(x > temp_min && x < temp_max)
        return x;
    else if(x <= temp_min)
        return temp_min;
    else
        return temp_max;
}

static void pumpOn(UArm *uarm)
{
    Xil_Out32(ADDR(PUMP_EN),HIGH);
    Xil_Out32(ADDR(VALVE_EN),LOW);
    uarm->status.pump = TRUE;
}

static void pumpOff(UArm *uarm)
{
    Xil_Out32(ADDR(PUMP_EN),LOW);
    Xil_Out32(ADDR(VALVE_EN),HIGH);
    uarm->status.pump = FALSE;
}

static void init(UArm *uarm,unsigned int addr)
{
    int i = 0;

	uarm->attr.base_address = addr;
    uarm->attr.offsetL = 0;
    uarm->attr.offsetR = 3;

    for(i = 0; i < 3; i ++){
    	uarm->attr.servo[i].pwm_min = D150A_SERVO_MIN_PUL;
    	uarm->attr.servo[i].pwm_max = D150A_SERVO_MAX_PUL;
    }

    uarm->attr.servo[3].pwm_min = D009A_SERVO_MIN_PUL;
    uarm->attr.servo[3].pwm_max = D009A_SERVO_MAX_PUL;

	uarm->status.pos.s = 100;
	uarm->status.pos.h = 50;
	uarm->status.pos.r = 0;

    pumpOff(uarm);


}



static void setSHR(UArm *uarm,double stretch,double height,int rot,int handrot)
{
    uarm->status.pos.s = stretch;
    uarm->status.pos.h = height;
    uarm->status.pos.r = rot;
    uarm->status.pos.handrot = handrot;

    setPosSHR(uarm,uarm->status.pos);

}

static void setXYZ(UArm *uarm,double x,double y,double z,int handrot)
{
    PosXYZ xyz;
    xyz.x = x;
    xyz.y = y;
    xyz.z = z;
    xyz.handrot = handrot;

    setPosXYZ(uarm,xyz);
}

static void XYtoSR(PosXYZ xyz,PosSHR *shr)
{
    double setx = xyz.x + 55;
    double x2y2 = setx * setx + xyz.y * xyz.y;
    shr->s = sqrt(x2y2) - 55;
    shr->r = (atan(xyz.y/(setx + 61))) * RAD_TO_DEG;
    shr->h = xyz.z;
    shr->handrot = xyz.handrot;

}

static void SRtoXY(PosSHR shr,PosXYZ *xyz)
{
    double r = shr.r / RAD_TO_DEG;
    double s = shr.s + 55;
    double a = 1 + tan(r) * tan(r);
    double b = 122 * tan(r) * tan(r);
    double c = 61 * 61 * tan(r) * tan(r) - s * s;

    double tx = s * cos(r);  //signal
    double x1 = (-b + sqrt(b * b - 4 * a * c))/(2 * a);
    double x2 = (-b - sqrt(b * b - 4 * a * c))/(2 * a);

    xyz->x = (tx * x1 > 0)? x1:x2;
    xyz->y = tan(r) * (xyz->x + 61);
    xyz->x -= 55;
    xyz->z = shr.h;
    xyz->handrot = shr.handrot;
}

static void setPosXYZ(UArm *uarm,PosXYZ xyz)
{
    XYtoSR(xyz,&uarm->status.pos);
    setPosSHR(uarm,uarm->status.pos);
}

static void formatSHR(PosSHR *shr)
{
    shr->s = constrain(shr->s, ARM_STRETCH_MIN,   ARM_STRETCH_MAX) + 55;		// +55, set stretch zero
    shr->h  = constrain(shr->h,  ARM_HEIGHT_MIN,    ARM_HEIGHT_MAX);
    shr->r  = constrain(shr->r,  ARM_ROTATION_MIN,  ARM_ROTATION_MAX) + 90;		// +90, change -90~90 to 0~180
    shr->handrot = constrain(shr->handrot, HAND_ROTATION_MIN, HAND_ROTATION_MAX) + 90;	// +90, change -90~90 to 0~180

}

static void setPosSHR(UArm *uarm,PosSHR shr)
{
    double s2h2,angleA,angleB,angleC;
    int angleR,angleL;
    uarm->status.pos = shr;
    shr.r = -shr.r;
    if(ifSwitchOn(uarm) && shr.h < uarm->attr.heightLst)
        shr.h = uarm->attr.heightLst;

    formatSHR(&shr);

    s2h2 = shr.s * shr.s + shr.h * shr.h;
    angleA = acos((ARM_A2B2 - s2h2) / ARM_2AB) * RAD_TO_DEG;
    angleB = atan(shr.h/shr.s) * RAD_TO_DEG;                         //
    angleC = acos((ARM_A2 + s2h2 -ARM_B2)/(2 * ARM_A * sqrt(s2h2))) * RAD_TO_DEG; //
    angleR = 180 - angleA - angleB - angleC + FIXED_OFFSET_R + uarm->attr.offsetR;        //
    angleL = angleB + angleC + FIXED_OFFSET_L + uarm->attr.offsetL;                       //
    // angle limit
    angleL = constrain(angleL, 10 + uarm->attr.offsetL, 145 + uarm->attr.offsetL);
    angleR = constrain(angleR, 25 + uarm->attr.offsetR, 150 + uarm->attr.offsetR);
    angleR = constrain(angleR, angleL - 90 + uarm->attr.offsetR, angleR);	// behind  -120+30 = -90

    if(angleL < 15 + uarm->attr.offsetL)
        angleR = constrain(angleR, 70 + uarm->attr.offsetR, angleR);

    setServo(uarm,SERVO_R, angleR);
    setServo(uarm,SERVO_L, angleL);
    setServo(uarm,SERVO_ROT, shr.r);
    setServo(uarm,SERVO_HANDROT, shr.handrot);

    uarm->attr.heightLst = shr.h;
}

static void setServo(UArm *uarm,char channel,int angle)
{
    unsigned int pwm_duty = uarm->attr.servo[channel].pwm_min + (uarm->attr.servo[channel].pwm_max - uarm->attr.servo[channel].pwm_min)/180 * angle;
    Xil_Out32(uarm->attr.base_address + 4 * channel,pwm_duty);
}

static char ifSwitchOn(UArm *uarm)
{
    if(!Xil_In32(ADDR(LIMIT_SW)))
        return TRUE;
    else
        return FALSE;
}






