/* Copyright (c) 2008 - 2009 Nokia Corporation
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */


#include <e32base.h>
#include <aknglobalnote.h>
#include <avkon.rsg>
#include "mem_wrapper.h"
#include "pythread.h"
#include <Python.h>

// This is a GCCE toolchain workaround needed when compiling with GCCE
// and using main() entry point
#ifdef __GCCE__
#include <staticlibinit_gcce.h>
#endif

_LIT(KProgressMessage, "Loading...");


int main(void)
{
    TInt error;
    char *runCmd = "import sys\n"
                   "import os\n"
                   "default_namespace = {'__builtins__': __builtins__, '__name__': '__main__'}\n"
                   "try:\n"
                   "    sys.path.insert(0, os.path.join(os.getcwd(), 'lib.zip'))\n"
                   "    execfile('default.py', default_namespace)\n"
                   "except SystemExit, err:\n"
                   "    if str(err) not in [str(0), '']:\n"
                   "        import traceback\n"
                   "        traceback.print_exc(None, sys.stdout)\n"
                   "        raw_input()\n"
                   "    else:\n"
                   "        sys.exit()\n"
                   "except:\n"
                   "    import traceback\n"
                   "    traceback.print_exc(None, sys.stdout)\n"
                   "    raw_input()\n"
                   "else:\n"
                   "    raw_input()\n";

    CActiveScheduler* scheduler = new (ELeave) CActiveScheduler();
    CActiveScheduler::Install(scheduler);
    
    SPy_DLC_Init();
    SPy_SetAllocator(SPy_DLC_Alloc, SPy_DLC_Realloc, SPy_DLC_Free, NULL);
    track_allocations(true);
    Py_Initialize();
    
    PyRun_SimpleString(runCmd);

    Py_Finalize();
    free_pthread_locks();
    free_all_allocations();
    SPy_DLC_Fini();

    return 0;
}
