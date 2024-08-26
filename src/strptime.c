#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <datetime.h>
#include <pyerrors.h>
#include <time.h>

static PyObject *
my_strptime(PyObject *self, PyObject *args)
{
    const char *datetime;
    const char *formatstr;
    struct tm tm = {0};
    const char *extraneous_chars;
    PyObject *py_datetime = NULL;

    if (!PyArg_ParseTuple(args, "ss", &datetime, &formatstr))
        return NULL;

    extraneous_chars = strptime(datetime, formatstr, &tm);

    if (extraneous_chars == NULL) {
        PyErr_SetString(PyExc_ValueError, "Date/time format did not match format string");
        return (PyObject *) NULL;
    }

    py_datetime = PyDateTime_FromDateAndTime(
            tm.tm_year + 1900,
            tm.tm_mon + 1,
            tm.tm_mday,
            tm.tm_hour,
            tm.tm_min,
            tm.tm_sec,
            0);

    if (py_datetime == NULL) {
        return NULL;
    }

    return py_datetime;
}

static PyMethodDef StrpMethods[] = {
    {"strptime",  my_strptime, METH_VARARGS,
     "Parse a time string."},
    {NULL, NULL, 0, NULL}        /* Sentinel */
};

static struct PyModuleDef strptimemodule = {
    PyModuleDef_HEAD_INIT,
    "strptime",
    "A module for parsing date/time values much faster.",
    -1,
    StrpMethods
};

PyMODINIT_FUNC
PyInit_strptime(void)
{
    PyDateTime_IMPORT;
    return PyModule_Create(&strptimemodule);
}

