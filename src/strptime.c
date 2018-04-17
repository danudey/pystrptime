#include <Python.h>
#include <python2.7/datetime.h>
#include <time.h>

static PyObject *
my_strptime(PyObject *self, PyObject *args)
{
    const char *datetime;
    const char *formatstr;
    struct tm tm;
    const char *extraneous_chars;
    PyObject *py_datetime = NULL;

    if (!PyArg_ParseTuple(args, "ss", &datetime, &formatstr))
        return NULL;
    
    extraneous_chars = strptime(datetime, formatstr, &tm);

    tm.tm_year += 1900;
    tm.tm_mon += 1;

    py_datetime = PyDateTime_FromDateAndTime(
            tm.tm_year,
            tm.tm_mon,
            tm.tm_mday,
            tm.tm_hour,
            tm.tm_min,
            tm.tm_sec,
            0);

    return py_datetime;
}

static PyMethodDef StrpMethods[] = {
    {"strptime",  my_strptime, METH_VARARGS,
     "Parse a time string."},
    {NULL, NULL, 0, NULL}        /* Sentinel */
};

PyMODINIT_FUNC
initstrptime(void)
{
    (void) Py_InitModule("strptime", StrpMethods);
    PyDateTime_IMPORT;
}

