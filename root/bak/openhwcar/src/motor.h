#ifndef MOTOR_HEADER
#define MOTOR_HEADER
struct CAR_STATE
{
	int ldir;
	int rdir;
	int lspd;
	int rspd;
};
enum ACTION{FORW,BACK,LEFT,RIGHT};
void car_init();
void left_wheel(int dir,int spd);
void right_wheel(int dir,int spd);
void car_set();
void move(enum ACTION act,int spd);
void stop();
extern struct CAR_STATE state;
#endif
