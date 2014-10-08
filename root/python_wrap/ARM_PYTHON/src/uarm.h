#ifndef UARM_H_INCLUDED
#define UARM_H_INCLUDED

#define SERVO_L 0
#define SERVO_R 1
#define SERVO_ROT 2
#define SERVO_HANDROT 3
#define PUMP_EN 4
#define VALVE_EN 5
#define LIMIT_SW 6

#define LOW 0
#define HIGH 1

#define TRUE 1
#define FALSE 0

/********************basic*******************/

#define ARM_A                   148    // upper arm
#define ARM_B                   160    // lower arm
#define ARM_2AB                 47360  // 2*A*B
#define ARM_A2                  21904  // A^2
#define ARM_B2                  25600  // B^2
#define ARM_A2B2                47504  // A^2 + B^2
#define ARM_STRETCH_MIN         0
#define ARM_STRETCH_MAX         210
#define ARM_HEIGHT_MIN          -180
#define ARM_HEIGHT_MAX          150
#define ARM_ROTATION_MIN        -90
#define ARM_ROTATION_MAX        90
#define HAND_ROTATION_MIN       -90
#define HAND_ROTATION_MAX       90

#define D150A_SERVO_MIN_PUL     535
#define D150A_SERVO_MAX_PUL     2415
#define D009A_SERVO_MIN_PUL     600
#define D009A_SERVO_MAX_PUL     2550

#define FIXED_OFFSET_L          18
#define FIXED_OFFSET_R          36

#define RAD_TO_DEG              57.2957786

double constrain(double x,double a,double b);

typedef struct PosXYZ
{
    double x,y,z;
    int handrot;
} PosXYZ;

typedef struct PosSHR
{
    double s,h;  //stretch height
    int r;         //rotate
    int handrot;
} PosSHR;

typedef struct UArmStatus
{
    PosSHR pos;
    char pump;     //true--on,false--off
    int speed;
} UArmStatus;

typedef struct UArmAttr
{
    unsigned int base_address;
    struct {
        unsigned short pwm_min;
        unsigned short pwm_max;
    } servo[4];
    short heightLst;
    unsigned char gripperRst;
    char offsetL;
    char offsetR;
} UArmAttr;


typedef struct UArm{

    //methods
    PosSHR (*getPosSHR)(struct UArm*);
	PosXYZ (*getPosXYZ)(struct UArm*);
	void (*getXYZ)(struct UArm*,double *x,double *y,double *z);
	void (*getSHR)(struct UArm*,double *s,double *h,double *r);
	int (*getHandrot)(struct UArm*);


	void (*setSHR)(struct UArm*,double stretch,double height,int rot,int handrot);  //set position by rotate
	void (*setXYZ)(struct UArm*,double x,double y,double z,int handrot); //set position by xyz

    void (*setPosSHR)(struct UArm*,PosSHR shr);
    void (*setPosXYZ)(struct UArm*,PosXYZ xyz);

    char (*ifSwitchOn)(struct UArm*);

    void (*pumpOn)(struct UArm *);
	void (*pumpOff)(struct UArm*);

    void (*init)(struct UArm*,unsigned int);

    UArmAttr attr;
    UArmStatus status;

    //values



} UArm;

UArm getUArm(unsigned int addr);



#endif // UARM_H_INCLUDED
