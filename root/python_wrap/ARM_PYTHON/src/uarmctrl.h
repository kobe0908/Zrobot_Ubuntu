#ifndef UARMCTRL_H_INCLUDED
#define UARMCTRL_H_INCLUDED

#include "uarm.h"

#define DEFAULT 0

typedef struct UArmCtrl{

    void (*setSpeed)(struct UArmCtrl*,int speed);

    void (*move)(struct UArmCtrl*,double x,double y,double z,int speed);

    void (*rothand)(struct UArmCtrl*,int handrot,int speed);

    void (*get)(struct UArmCtrl*,int speed);

    void (*put)(struct UArmCtrl*,int speed);

    int speed;

    UArm uarm;

} UArmCtrl;

UArmCtrl getUArmCtrl();


#endif // UARMCTRL_H_INCLUDED
