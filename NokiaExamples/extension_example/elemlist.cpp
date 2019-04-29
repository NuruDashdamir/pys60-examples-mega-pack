/*
   Copyright (c) 2005 Nokia
   Programming example -- see license agreement for additional rights
   A simple extension used in the Porting an Extension example.
*/

/* 
   This extension module implements a new native type, the "cons
   cell", that is very similar to the cons cells used in Lisp.

   This code illustrates some of the issues that arise when creating
   extensions for Python for Series 60.  The code is derived from the
   example extension written by Alex Martelli for the Python
   Cookbook. The original code is licensed under the Python license,
   which is available at http://www.python.org/license.

   All parts that had to be modified from the original have
   been clearly marked. A summary of modifications:

   - Since Symbian DLL's don't (properly) support global writable
   data, the type object is allocated dynamically and filled in from a
   const template. Also, the function table for the module has been
   declared const.

   - The macro versions of memory allocation routines (PyObject_NEW,
   PyObject_DEL and others) are not supported in Python for Series 60
   1.0, so the non-macro versions, PyObject_New, PyObject_Del must be
   used instead.

   - The file has been compiled with the C++ compiler, to make it
   possible to include Symbian headers. 
*/

#include "Python.h"

/*******************************************************
 This include file declares the SPyGetGlobalString and 
 SPySetGlobalString functions: */
#include "symbian_python_ext_util.h"
/* Standard Symbian definitions: */
#include <e32std.h>
/*******************************************************/

/* type-definition & utility-macros */
typedef struct {
    PyObject_HEAD
    PyObject *car, *cdr;
} cons_cell;


/*******************************************************
   Original definition:
   staticforward PyTypeObject cons_type; 

   Symbian doesn't support writable global data in DLL's, so
   this type object has to be stored in another way.  We
   choose to allocate it dynamically in the module init
   function and to bind it to a global name, so that we can
   access it with the SPyGetGlobalString function.  For
   convenience, we define a macro that encapsulates the use
   of that function. Naming a macro in all lowercase
   violates the standard naming convention for macros, but
   allows you to keep the code that handles the type
   unchanged, which may be convenient if the same source
   code is used on multiple platforms. You will have to
   decide for yourself if this is too unsavoury for your
   tastes. */
#define cons_type (*(PyTypeObject *)SPyGetGlobalString("consType"))
/*******************************************************/


/* a typetesting macro (we don't use it here) */
#define is_cons(v) ((v)->ob_type == &cons_type)
/* macros to access car & cdr, both as lvalues & rvalues */
#define carof(v) (((cons_cell*)(v))->car)
#define cdrof(v) (((cons_cell*)(v))->cdr)

/* ctor (factory-function) and dtor */
static cons_cell*
cons_new(PyObject *car, PyObject *cdr)
{
    /*******************************************************
     Original code: 
       cons_cell *cons = PyObject_NEW(cons_cell, &cons_type);
     The macro versions of memory allocation routines 
     (PyObject_NEW, PyObject_DEL and others) are not supported
     in Python for Series 60 1.0, so the non-macro versions,
     PyObject_New, PyObject_Del must be used instead. 

     The Python documentation states that the use of these macros in
     extensions is bad practice in any case, since it ties the
     extension to the behaviour of the interpreter in unpredictable
     ways. */
    cons_cell *cons = PyObject_New(cons_cell, &cons_type);
    /*******************************************************/
    if(cons) {
        cons->car = car; Py_INCREF(car);  /* INCREF when holding a PyObject* */
        cons->cdr = cdr; Py_INCREF(cdr);  /* ditto */
    }
    return cons;
}
static void
cons_dealloc(cons_cell* cons)
{
    /* DECREF when releasing previously-held PyObject*'s */
    Py_DECREF(carof(cons)); Py_DECREF(cdrof(cons));
    /*******************************************************
     Original code: 
       PyObject_DEL(cons);
     See the note on PyObject_NEW.*/
    PyObject_Del(cons);
    /*******************************************************/
}

/* Python type-object */

/*******************************************************
   Original definition:
   statichere PyTypeObject cons_type = {

   As mentioned above, Symbian doesn't support _writable_
   global data in DLL's, so we store this partially
   initialized type object as constant data. In the module
   init function this is copied to a dynamically allocated,
   writable memory region. Note the name change to avoid 
   clashing with the macro cons_type defined above. */
static const PyTypeObject cons_type_template = {
/*******************************************************/
    PyObject_HEAD_INIT(0)    /* initialize to 0 to ensure Win32 portability */
    0,                 /*ob_size*/
    "cons",            /*tp_name*/
    sizeof(cons_cell), /*tp_basicsize*/
    0,                 /*tp_itemsize*/
    /* methods */
    (destructor)cons_dealloc, /*tp_dealloc*/
    /* implied by ISO C: all zeros thereafter */
};

/* module-functions */
static PyObject*
cons(PyObject *self, PyObject *args)    /* the exposed factory-function */
{
    PyObject *car, *cdr;
    if(!PyArg_ParseTuple(args, "OO", &car, &cdr))
        return 0;
    return (PyObject*)cons_new(car, cdr);
}
static PyObject*
car(PyObject *self, PyObject *args)     /* car-accessor */
{
    PyObject *cons;
    if(!PyArg_ParseTuple(args, "O!", &cons_type, &cons))  /* type-checked */
        return 0;
    return Py_BuildValue("O", carof(cons));
}
static PyObject*
cdr(PyObject *self, PyObject *args)     /* cdr-accessor */
{
    PyObject *cons;
    if(!PyArg_ParseTuple(args, "O!", &cons_type, &cons))  /* type-checked */
        return 0;
    return Py_BuildValue("O", cdrof(cons));
}
/*******************************************************
   Original definition:
   static PyMethodDef elemlist_methods[] = {
 
   Since no one needs to write to this particular array,
   we can make the code work simply by adding "const". 
   There's no need to copy the data. */
static const PyMethodDef elemlist_methods[] = {
/*******************************************************/
    {"cons",   cons,   METH_VARARGS},
    {"car",    car,    METH_VARARGS},
    {"cdr",    cdr,    METH_VARARGS},
    {0, 0}
};

/* module entry-point (module-initialization) function */
/*******************************************************
   Original definition:
   void initelemlist(void)
 
   We have to explicitly state that this function must be
   included in the public function list of the DLL. Symbian
   DLL's don't include names of the exported functions; the
   program that loads a DLL has to know the the index of the
   function in the function table, commonly known as the
   ordinal of the function, to call the functions in the
   DLL. 

   The initialization function for a Python module _must_ be
   exported at ordinal 1. If the module exports just the
   initializer function, then there is nothing to worry
   about. If you also export a module finalizer function,
   you will have to make sure that the initializer is
   exported at ordinal 1 and the finalizer at ordinal 2.

   This module has just the initializer function. 

   Also, the function has to be declared extern "C":*/
extern "C" {
DL_EXPORT(void) initelemlist(void)
/*******************************************************/
{
    /* Create the module and add the functions */
    /*******************************************************
      Original code:
        PyObject *m = Py_InitModule("elemlist", elemlist_methods);
      The Python/C API is unfortunately not quite const-correct, so 
      we need to add a cast here to make the compiler happy:*/
    PyObject *m = Py_InitModule("elemlist", (PyMethodDef*)elemlist_methods);
    /*******************************************************/

    /* Finish initializing the type-objects */
    
    /*******************************************************
     Allocate storage for the type object, fill it in
     from the constant template and bind it to a name in the
     module namespace: */    
    PyTypeObject *consTypeObject=PyObject_New(PyTypeObject, &PyType_Type);
    *consTypeObject=cons_type_template;
    SPyAddGlobalString("consType", (PyObject *)consTypeObject);
    /*******************************************************/
    
    cons_type.ob_type = &PyType_Type;
}
}

/*******************************************************
 This function is mandatory in Symbian DLL's. */

GLDEF_C TInt E32Dll(TDllReason)
{
  return KErrNone;
}
/*******************************************************/
