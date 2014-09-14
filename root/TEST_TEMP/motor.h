#ifndef MOTOR_HEADER
#define MOTOR_HEADER
struct CAR_STATE
{
	long lspd;
	long  rspd;
};
void display();
enum ACTION{FORW,BACK,LEFT,RIGHT};
void car_init();
void left_wheel(long spd);
void right_wheel(long spd);
void car_set();
void move(int  act,long spd);
void stop();
extern struct CAR_STATE state;
#endif
