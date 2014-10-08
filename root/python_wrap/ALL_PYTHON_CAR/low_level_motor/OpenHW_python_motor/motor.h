#ifndef MOTOR_HEADER
#define MOTOR_HEADER
struct CAR_STATE
{
	long lspd;
	long  rspd;
};

void car_init();
void left_wheel(long spd);
void right_wheel(long spd);
void car_set();
void move(int act,long spd);
void stop();
void position_ctrl(int wheelL_set, int wheelR_set, int wheelL_speed, int wheelR_speed);
extern struct CAR_STATE state;
#endif
