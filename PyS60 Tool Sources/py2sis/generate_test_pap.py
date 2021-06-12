# Copyright (c) 2009 Nokia Corporation
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

import os
import shutil

sis_list = " "
topdir = "..\\..\\.."
testapp_sis = ""
my_dirs = []


def parse_ensymble_options(test_file, fp):
    # Find the ensymble options associated with test script, in options.txt
    line = fp.readline().strip('\n')
    while line:
        test_script, ensymble_options = line.split(':')
        if test_script + ".py" == test_file:
            return ensymble_options
        line = fp.readline().strip('\n')
    return ""


def copy_modules():
    # Copy the modules created for testing to module-repo folder
    for dirname in os.listdir('..\\test_package'):
        if dirname not in ["test_scripts", ".svn"]:
            my_dirs.append(dirname)
            shutil.copytree('..\\test_package\\' + dirname, \
                'module-repo\\dev-modules\\' + dirname + "\\" + dirname)

for testapp in os.listdir(topdir + '\\build\\test\\'):
    # Search for testapp sis white choco variant
    if testapp.startswith('testapp_') and testapp.endswith('_white_choco.sis'):
        testapp_sis = testapp

if testapp_sis:
    # Create and embed the test sis only if testapp is present
    copy_modules()
    for filename in os.listdir('..\\test_package\\test_scripts'):
        if filename != 'options.txt' and filename != '.svn':
            fp = open('..\\test_package\\test_scripts\\options.txt', 'r')
            ensymble_options = parse_ensymble_options(filename, fp)
            fp.close()
            os.system('python ensymble.py py2sis ' + \
                ensymble_options + ' ..\\test_package\\test_scripts' + \
                '\\' + filename)
            sis_list = sis_list + \
                filename.split('.')[0] + '_v1_0_0.sis '
    os.system('python ensymble.py mergesis --cert=' + \
        topdir + '\\..\\keys\\pythonteam_pem.crt --privkey=' + \
        topdir + '\\..\\\keys\\pythonteam.key --passphrase=12345 ' + \
        topdir + '\\build\\test\\' + testapp_sis + sis_list + testapp_sis)

    # Move the merged testapp sis to the build artifacts-test directory and
    # remove the generated test sis and clean up the modules copied to module-repo
    # folder
    shutil.move(testapp_sis, topdir + '\\build\\test\\' + testapp_sis)
    for sis_files in os.listdir(os.getcwd()):
        if sis_files.startswith('test_') and sis_files.endswith('.sis'):
            os.remove(sis_files)
    for _dir in my_dirs:
        os.system('rmdir /S/Q ' + 'module-repo\\dev-modules\\' + _dir)
