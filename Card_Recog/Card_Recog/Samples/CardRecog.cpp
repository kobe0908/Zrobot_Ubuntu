/*
 Project:		Lane Detect Class for Smart Car Applications
 Author:		Jerry Peng
 Created on:	Mar 20,2014
*/

#include <opencv2/opencv.hpp>
#include <iostream>
#include <vector>
#include <iterator>

using namespace std;
using namespace cv;



int colorDetect(Mat src);


  int main(int argc, const char** argv)
 {


	 VideoCapture cap(0);
	 if( !cap.isOpened() ){
		cout << "Could not initialize capturing...\n";
        return -1;
	}

	int thres1 = 0;
	int thres2 = 80;
	int thresArea = 100;
	int thresCircleFactor = 150;

	namedWindow("controlPanel");
	createTrackbar( "thres1", "controlPanel", &thres1, 255, 0);
	createTrackbar( "thres2", "controlPanel", &thres2, 255, 0);
	createTrackbar( "area", "controlPanel", &thresArea, 255, 0);
	createTrackbar( "circleFactor", "controlPanel", &thresCircleFactor, 255, 0);

	int detectNum = 0;

	Mat frame;
	Mat gray;
	Mat canny;
	Mat sub;
	Mat BW;
	for(;;){

		cap>>frame;
		cvtColor(frame, gray, CV_RGB2GRAY);
		imshow("beforeBlur", gray);
		GaussianBlur(gray, gray, Size(7,7), 1.5, 1.5);
		imshow("afterBlur", gray);
		Canny(gray, canny, thres1, thres2);
		imshow("canny",canny);



		vector<vector<Point> > contours;
		vector<vector<Point> >::iterator itc;
		findContours(canny, contours, CV_RETR_LIST, CV_CHAIN_APPROX_NONE);
		itc = contours.begin();

		// find minimum match value
		double min = 100.0f;

		double circleFactor_thres = (double)thresCircleFactor/500;
		while(itc!= contours.end()) {  
			// Feature Extract 
			
			double area = contourArea(*itc);
			bool isClosed=true;
			double perimeter = arcLength(*itc,isClosed);
			double circleFactor = 4*3.1415926*area/(perimeter*perimeter);
			

					if(  isContourConvex(*itc) || area<thresArea*15 || circleFactor>circleFactor_thres)				
						itc=contours.erase(itc);
					else
						++itc;
		}


		Mat result;
		frame.copyTo(result);
		drawContours(result, contours, -1, Scalar(0,255,0), 4);
		

		int maxSize = 0;
		itc = contours.begin();
		while(itc!= contours.end()) {             //find the max contour size
					if(itc->size() > maxSize)
						maxSize = itc->size();
					++itc;
		}

		itc = contours.begin();
		while(itc!= contours.end()) {             //Eliminate smaller contours
						if(itc->size() < maxSize)
							itc=contours.erase(itc);
						else
						++itc;
			}

		itc = contours.begin();
		if(itc != contours.end()){
			double area = contourArea(*itc);
			bool isClosed=1;
			double perimeter = arcLength(*itc,isClosed);
			double circleFactor = 4*3.1415926*area/(perimeter*perimeter);
			cout<<circleFactor<<endl;
		}

		Mat leftContour(canny.size(), CV_8UC3, Scalar(0,0,0));
		drawContours(leftContour, contours, -1, Scalar(255,255,255), CV_FILLED);
		Mat NumArea(canny.size(), CV_8UC3, Scalar(0,0,0));
		NumArea = frame & leftContour;
		Mat hsv;
		//cvtColor(NumArea, hsv,CV_BGR2HSV);
		imshow("NumArea", NumArea);

		int tempDetectNum = colorDetect(NumArea);
		if(tempDetectNum == 1) detectNum =1;
		if(tempDetectNum == 2) detectNum =2;
		if(tempDetectNum == 5) detectNum =5;

		//char label[20];
		//sprintf(label, "Detected Num:%d",detectNum );
		//putText(result,label,Point(10,30),FONT_HERSHEY_SIMPLEX,1,Scalar(0,255,0),2,8);
		//putText(result,label,Point(10,55),FONT_HERSHEY_SIMPLEX,1,Scalar(255,0,0),2,8);
		//putText(result,label,Point(10,80),FONT_HERSHEY_SIMPLEX,1,Scalar(0,0,255),2,8);

		imshow("result_draw", result);
		if(waitKey(33) == 27) break;
	}

	return 0;
}


int colorDetect(Mat src){
	int colorIndex;
	double blue=0, red=0, green=0;

	for( int j= 0; j< src.size().height; j++){
			for( int i= 0; i< src.size().width; i++){
					blue += src.at<Vec3b>(j,i)[0];
					green += src.at<Vec3b>(j,i)[1];
					red += src.at<Vec3b>(j,i)[2];
			}
		}

	cout<<"Red:"<<red<<"; Green:"<<green<<"; Blue:"<<blue<<endl;

	if(blue>red && blue>green) colorIndex = 5;
	else if(green+blue>red && red+blue>green) colorIndex = 2;
	else if(red>blue && red>green) colorIndex = 1;
	else colorIndex = 0;

	return colorIndex;

}
