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
import sys
import shutil
import win32con
import win32api
import zipfile
from subprocess import call, STDOUT


class BuildFailedException(Exception):
    pass

def deltree(top):
    for root, dirs, files in os.walk(top, topdown=False):
        for name in files:
            win32api.SetFileAttributes(os.path.join(root, name),
                                       win32con.FILE_ATTRIBUTE_NORMAL)
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))
    os.rmdir(top)


def unzip_file_into_dir(file, dir):
    if not os.path.exists(dir):
        os.mkdir(dir, 0777)
    zfobj = zipfile.ZipFile(file)
    if not os.path.isdir(dir):
        os.makedirs(dir)
    for name in zfobj.namelist():
        print 'Unzipping: ', os.path.abspath(os.path.join(dir, name))
        if name.endswith('/') and \
                 not os.path.exists(os.path.abspath(os.path.join(dir, name))):
            os.makedirs(os.path.abspath(os.path.join(dir, name)))
        else:
            temp = os.path.join(os.path.abspath(dir), name)
            if not os.path.isdir(os.path.abspath(temp)):
                print 'Unzipping: ', os.path.abspath(temp)
                dirname = os.path.dirname(temp)
                if not os.path.exists(dirname):
                    os.makedirs(dirname)
                outfile = open(os.path.abspath(temp), 'wb')
                outfile.write(zfobj.read(name))
                outfile.close()


def create_clean_env(epoc32_zip):
    epoc_path = '\\Epoc32'
    if os.path.exists(epoc_path):
        shutil.rmtree(epoc_path)
    unzip_file_into_dir(epoc32_zip, '\\')
