#include "cv.h"  
#include "highgui.h"  
#include <iostream>  

using namespace std;
 
int main()  
{  
IplImage *src_img =cvLoadImage("/test.jpg",-1);
IplImage *dst_img;  
cout<<"******************************"<<endl<<endl;  
cout<<"The information"<<endl<<endl;  
cout<<"Size:"<<src_img->nSize<<endl;
cout<<"ID:"<<src_img->ID<<endl;
cout<<"Channels:"<<src_img->nChannels<<endl;
cout<<"Dataorder"<<src_img->dataOrder<<endl;
cout<<"Original"<<src_img->origin<<endl;
cout<<"Depth:"<<src_img->depth<<endl;
cout<<"Width"<<src_img->width<<endl;
cout<<"Height"<<src_img->height<<endl;
cout<<"ROI:"<<src_img->roi<<endl;
cout<<"WidthStep"<<src_img->widthStep<<endl; 
cout<<"ImageSize"<<src_img->imageSize<<endl;

return 0;

}
