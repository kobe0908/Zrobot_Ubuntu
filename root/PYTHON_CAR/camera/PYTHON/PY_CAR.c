#include "./src/eye.h"
#include "./src/roadctl.h"
#include "./src/sign.h"
#include <stdio.h>
void opencamera()
{
    printf("The camera is on!\n");
    eye_open();
}
void closecamera()
{
    printf("The camera is off!\n");
    eye_close();
}
void camera_analyze()
{
    printf("We provide some analyze method about tracing the sign!\n");
    sharingan();
}
void camera_record()
{
    printf("The camera is recoding now!\n");
    blink();
}
void camera_initialsign()
{
    printf("The camera will find the sign soon\n");
    sign_init();
}
void camera_cleansign()
{
    printf("The sign which has been recoded will be removed and refind the sign!\n");
    sign_clean();
}
void camera_recognizesign()
{
    printf("We provide the sign recognition methods! \n");
    reg_sign();
}
void camera_errsign()
{
    printf("We provide the methods about calculation the error between the car and the sign\n");
    sign_err();
}
void camera_errplane()
{
    printf("We provide the methods to calculate the distance between the sign and the road\n");
    plane_err();
}
void camera_adjustment()
{
    printf("We provide the methods to make the adjustment between the sign and the road");
    adjust_err();
}







