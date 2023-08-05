#define PY_SSIZE_T_CLEAN
#include <Python.h>

#include "sdnoise1234.h"
#include "srdnoise23.h"

static PyObject* sdnoise_sdnoise1(PyObject *self, PyObject *args)
{
    float x;

    if (!PyArg_ParseTuple(args, "f", &x))
        return NULL;

    float dx;
    float n = sdnoise1(x, &dx);

    return Py_BuildValue("ff", n, dx);
}

static PyObject* sdnoise_sdnoise2(PyObject *self, PyObject *args)
{
    float x, y;

    if (!PyArg_ParseTuple(args, "ff", &x, &y))
        return NULL;

    float dx, dy;
    float n = sdnoise2(x, y, &dx, &dy);

    return Py_BuildValue("fff", n, dx, dy);
}

static PyObject* sdnoise_sdnoise3(PyObject *self, PyObject *args)
{
    float x, y, z;

    if (!PyArg_ParseTuple(args, "fff", &x, &y, &z))
        return NULL;

    float dx, dy, dz;
    float n = sdnoise3(x, y, z, &dx, &dy, &dz);

    return Py_BuildValue("ffff", n, dx, dy, dz);
}

static PyObject* sdnoise_sdnoise4(PyObject *self, PyObject *args)
{
    float x, y, z, w;

    if (!PyArg_ParseTuple(args, "ffff", &x, &y, &z, &w))
        return NULL;

    float dx, dy, dz, dw;
    float n = sdnoise4(x, y, z, w, &dx, &dy, &dz, &dw);

    return Py_BuildValue("fffff", n, dx, dy, dz, dw);
}

static PyObject* sdnoise_srdnoise2(PyObject *self, PyObject *args)
{
    float x, y, t;

    if (!PyArg_ParseTuple(args, "fff", &x, &y, &t))
        return NULL;

    float dx, dy;
    float n = srdnoise2(x, y, t, &dx, &dy);

    return Py_BuildValue("fff", n, dx, dy);
}

static PyObject* sdnoise_srdnoise3(PyObject *self, PyObject *args)
{
    float x, y, z, t;

    if (!PyArg_ParseTuple(args, "ffff", &x, &y, &z, &t))
        return NULL;

    float dx, dy, dz;
    float n = srdnoise3(x, y, z, t, &dx, &dy, &dz);

    return Py_BuildValue("ffff", n, dx, dy, dz);
}

static PyMethodDef sdnoise_methods[] =
{
    {"sdnoise1", sdnoise_sdnoise1, METH_VARARGS, "Calculate Simplex 1D noise with gradients."},
    {"sdnoise2", sdnoise_sdnoise2, METH_VARARGS, "Calculate Simplex 2D noise with gradients."},
    {"sdnoise3", sdnoise_sdnoise3, METH_VARARGS, "Calculate Simplex 3D noise with gradients."},
    {"sdnoise4", sdnoise_sdnoise4, METH_VARARGS, "Calculate Simplex 4D noise with gradients."},
    {"srdnoise2", sdnoise_srdnoise2, METH_VARARGS, "Calculate Simplex 2D noise with rotated gradients."},
    {"srdnoise3", sdnoise_srdnoise3, METH_VARARGS, "Calculate Simplex 3D noise with rotated gradients."},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef sdnoise_module =
{
    PyModuleDef_HEAD_INIT,
    "sdnoise",
    NULL,
    -1,
    sdnoise_methods
};

PyMODINIT_FUNC PyInit_sdnoise(void)
{
    return PyModule_Create(&sdnoise_module);
}
