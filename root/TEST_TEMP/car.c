#include <Python.h>
#include <stdio.h>
#include "xil_io.h"
#include "motor.h"

#define XPAR_MOTOR_CTRL_L_MOTOR_S_AXI_BASEADDR 0x43C01000
#define XPAR_MOTOR_CTRL_R_MOTOR_S_AXI_BASEADDR 0x43C02000
#define FORW 1;
#define BACK 2;
#define LEFT 3;
#define RIGHT 4;

struct CAR_STATE state;

int cur_posL;
int cur_posR;
static PyObject* car_debug(PyObject* self, PyObject* args)
{
	display();
	Py_RETURN_NONE;
}
static PyObject* car_initial(PyObject* self, PyObject* args)
{
	void car_init();
	printf("the initial is okay");
	Py_RETURN_NONE;
}

static PyObject* car_mov(PyObject* self, PyObject* args)
{
	int act;
	long spd;
	if (!PyArg_ParseTuple(args,"il",&act,&spd))
	{
		return NULL;
	}
	printf("memory is okay \n");
	void move(int act,long spd);
}

static PyObject* car_stop(PyObject* self, PyObject* args)
{
	void stop();
	Py_RETURN_NONE;
}

static PyObject* car_control(PyObject* self, PyObject* args)
{
	int wheelL_set, wheelR_set, wheelL_speed,  wheelR_speed;
	void position_ctrl(int wheelL_set, int wheelR_set, int wheelL_speed, int wheelR_speed);
}

static PyMethodDef car_methods[]=
{
	{"move",(PyCFunction)car_mov,METH_VARARGS,NULL},
	{"init",(PyCFunction)car_initial,METH_NOARGS,NULL},
	{"stop",(PyCFunction)car_stop,METH_NOARGS,NULL},
	{"control",(PyCFunction)car_control,METH_VARARGS,NULL},
	{"display",(PyCFunction)car_debug,METH_NOARGS,NULL},
	{NULL,NULL,0,NULL},
};

PyMODINIT_FUNC initcar()
{
	Py_InitModule3("car",car_methods,"car move in python");
}
