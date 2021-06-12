# Copyright (c) 2005-2009 Nokia Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os.path
import sys
import re
import glob
from shellutil import *

sys.path.append(os.path.join(os.getcwd(), 'tools'))

emu_release_from = '\\epoc32\\release\\' + EMU_PLATFORM + '\\' + EMU_BUILD
emu_release_to = 'epoc32\\release\\' + EMU_PLATFORM + '\\' + EMU_BUILD
rsc_files = '\\z\\private\\10003A3F\\apps'
dev_release_from = '\\epoc32\\release\\' + DEVICE_PLATFORM + '\\'
dev_release_to = 'epoc32\\release\\' + DEVICE_PLATFORM + '\\'
pyd_mmp_files = []
SDK_FILES = []
pyd_mmp_path = ['newcore\\Symbian\\group']
if INCLUDE_INTERNAL_SRC and S60_VERSION != 30:
    pyd_mmp_path.append('..\\internal-src\scriptext\\group')

skipped_mmp_files = ['python25', 'appui', 'python_ui', 'Python_launcher',
                     'start_exe_testapp', '_sensorfw', '_sensor']

for r, p, f in os.walk("ext\\amaretto\\"):
    for dirs in p:
        pathname = os.path.join(r, dirs)
        if re.search("group$", pathname):
            pyd_mmp_path.append(pathname)

for entry in (
    {'from': emu_release_from,
     'to': emu_release_to,
     'files': ['python25.dll', 'python25.lib', 'testapp.exe',
                PREFIX + 'Python_appui.dll', 'Python_ui.exe',
                PREFIX + 'Python_launcher.exe', 'start_exe_testapp.exe']},
    {'from': emu_release_from + rsc_files,
     'to': emu_release_to + rsc_files,
     'files': ['testapp_reg.RSC']},
    {'from': dev_release_from + DEVICE_BUILD,
     'to': dev_release_to + DEVICE_BUILD,
     'files': ['python25.dll', 'testapp.exe', PREFIX + 'Python_launcher.exe',
               'start_exe_testapp.exe', PREFIX + 'Python_appui.dll']},
    {'from': dev_release_from + 'LIB',
     'to': dev_release_to + 'LIB',
     'files': [PREFIX + 'Python_appui.dso',
               PREFIX + 'Python_appui{000a0000}.dso', 'python25.dso',
               'python25{000a0000}.dso', PREFIX + 'Python_appui.lib',
               PREFIX + 'Python_appui{000a0000}.lib', 'python25.lib',
               'python25{000a0000}.lib']},
    {'from': '\\epoc32\\release\\winscw\\udeb\\' + rsc_files,
     'to': 'epoc32\\release\\winscw\\udeb\\' + rsc_files,
     'files': ['testapp_reg.RSC', 'Python_ui_reg.rsc']},
    {'from': '\\epoc32\\release\\winscw\\udeb\\z\\resource\\apps',
     'to': 'epoc32\\release\\winscw\\udeb\\\z\\resource\\apps',
     'files': ['Python_ui.rsc', PREFIX + 'appuifwmodule.rsc',
               'Python_ui_aif.mif', 'Python_ui_loc.rsc']},
    {'from': '\\epoc32\\data\\z\\resource\\apps',
     'to': 'epoc32\\data\\z\\resource\\apps',
     'files': [PREFIX + 'appuifwmodule.rsc']},
    {'from': '\\epoc32\\include',
     'to': 'epoc32\\include',
     'files': ['Python_ui.rsg', PREFIX + 'appuifwmodule.rsg']}):
    for f in entry['files']:
        SDK_FILES.append((os.path.normpath(entry['from'] + '\\' + f),
                          os.path.normpath(entry['to'] + '\\' +
                                           os.path.basename(f))))

for folders in pyd_mmp_path:
    pyd_mmp_files += files_matching_regex(folders, '(.*\.mmp$)')

for mmp_file in pyd_mmp_files:
    file_name, ext = os.path.basename(mmp_file).split('.')
    pyd_file = None
    if file_name == 'gps':
        pyd_file = PREFIX + "_locationacq.pyd"
    elif file_name not in skipped_mmp_files:
        pyd_file = PREFIX + file_name + ".pyd"
    if pyd_file is not None:
        SDK_FILES.append(((emu_release_from + '\\' + pyd_file),
                          (emu_release_to + '\\' + pyd_file)))
    else:
        print "Skipping mmp file:", mmp_file

for header_file in files_matching_regex('\\epoc32\\include\\python25',
                                        '.*.h'):
    SDK_FILES.append((header_file, ('epoc32\\include\\python25\\' +
                                     os.path.basename(header_file))))

for lib_file in files_matching_regex('\\epoc32\\winscw\\c\\resource\\python25',
                                     '.*'):
    temp_path, relative_lib_file = lib_file.split('resource\\python25\\')
    SDK_FILES.append((lib_file, ('epoc32\\winscw\\c\\resource\\python25\\' +
                                  relative_lib_file)))

# This loop is for copying all the files in c\\data\\python\\ folder.
for dependent_files in files_matching_regex('\\epoc32\\winscw\\c\\data\\' +
                                            'python', '.*'):
    temp_path, relative_dependent_file = dependent_files.split('data\\' +
                                                               'python\\')
    SDK_FILES.append((dependent_files, ('epoc32\\winscw\\c\\data\\python\\' +
                                         relative_dependent_file)))

# This loop is for copying all the files in c\\data\\test\\ folder. This
# folder structure is required by test_zipfile.
for dependent_files in files_matching_regex('\\epoc32\\winscw\\c\\data\\test',
                                            '.*'):
    temp_path, relative_dependent_file = dependent_files.split('data\\test\\')
    SDK_FILES.append((dependent_files, ('epoc32\\winscw\\c\\data\\test\\' +
                                         relative_dependent_file)))
if INCLUDE_ARMV5_PYDS:
    binary_from = dev_release_from + DEVICE_BUILD
    binary_to = dev_release_to + DEVICE_BUILD
    for dependent_files in files_matching_regex(binary_from + '\\', '.*.pyd'):
        temp_path, relative_dependent_file = \
                                        dependent_files.split('armv5\\urel\\')
        SDK_FILES.append((dependent_files, (binary_to + '\\' +
                                              relative_dependent_file)))
    if BUILD_PROFILE == 'release':
        SDK_FILES.append(((binary_from + '\\run_testapp.exe'),
                          (binary_to + '\\run_testapp.exe')))
        SDK_FILES.append(((binary_from + '\\interpreter-startup.exe'),
                          (binary_to + '\\interpreter-startup.exe')))
        SDK_FILES.append(((binary_from + '\\run-interpretertimer.exe'),
                          (binary_to + '\\run-interpretertimer.exe')))

        rsc_file_path = 'private\\10003a3f\\import\\apps\\'

        SDK_FILES.append((('\\Epoc32\\Data\\z\\' + rsc_file_path +
                           'testapp_reg.RSC'),
                          ('Epoc32\\Data\\z\\' + rsc_file_path +
                           'testapp_reg.RSC')))
        SDK_FILES.append((('\\Epoc32\\Data\\z\\' + rsc_file_path +
                           'run_testapp_reg.rsc'),
                          ('Epoc32\\Data\\z\\' + rsc_file_path +
                           'run_testapp_reg.rsc')))
        SDK_FILES.append((('\\Epoc32\\Data\\z\\' + rsc_file_path +
                           'interpreter-startup_reg.RSC'),
                          ('Epoc32\\Data\\z\\' + rsc_file_path +
                           'interpreter-startup_reg.RSC')))
        SDK_FILES.append((('\\Epoc32\\Data\\z\\' + rsc_file_path +
                           'run-interpretertimer_reg.RSC'),
                          ('Epoc32\\Data\\z\\' + rsc_file_path +
                           'run-interpretertimer_reg.RSC')))


SDK_FILES.append((('\\epoc32\\winscw\\c\\private\\' + PYS60_UID_PYTHONUI[2:] +
                   '\\launcher.py'),
                  ('epoc32\\winscw\\c\\private\\' + PYS60_UID_PYTHONUI[2:] +
                   '\\launcher.py')))
SDK_FILES.append((('\\epoc32\\winscw\\c\\private\\' + PYS60_UID_PYTHONUI[2:] +
                   '\\default.py'),
                  ('epoc32\\winscw\\c\\private\\' + PYS60_UID_PYTHONUI[2:] +
                   '\\default.py')))
