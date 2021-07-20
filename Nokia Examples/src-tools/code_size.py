# Copyright (c) 2008 Nokia Corporation
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

# This script calculates the code size of the dll, pyd's and the python runtime
# sis, which is displayed graphically in project metrics tab of release build.

import sys
import os
import time

# `metrics_data`: map format -> {binary_type: (path, extension)}
# 'binary_type' are the metrics for which code size is calculated.The value
# for these keys comprise of the path along with the extension(if specified),
# to the respective 'binary_type'.
metrics_data = {'Python25.dll':
                    ('\\epoc32\\release\\armv5\\urel\\python25.dll', ''),
                'Other PYDs': ('\\epoc32\\release\\armv5\\urel\\', 'pyd')}
binary_size = {}


def file_size(file_path):
    file_stat = os.stat(file_path)
    return (file_stat.st_size) / 1024.00   # Get size of file in kilobytes


def print_metrics(log_file, release):
    log = open(log_file, 'a+')
    now = time.strftime("%b %d %Y %H:%M:%S")  # Get date, time when writing log
    log_string = "Time=%s,Release=%s," % (now, release)
    for code in binary_size:
        log_string += "%s=%f," % (code, binary_size[code])
    log.write(log_string + "\n")
    log.close()


def updatelog(release, python_runtime, log_file):
# This function is called to log the code size, something like this
# code_size.log(platform, python_runtime, "C:\\logs\\code_size.log")
    global binary_size
    metrics_data['Python25_runtime.sis'] = (python_runtime, '')
    for binary_type in metrics_data:
        binary_path, file_ext = metrics_data[binary_type]
        if "pyd" in file_ext:
            all_files = os.listdir(binary_path)
            total_size = 0
            for afile in all_files:
                if afile.endswith(".pyd"):
                    total_size += file_size(os.path.join(binary_path, afile))
            binary_size[binary_type] = total_size
        elif not file_ext:  # Either sis or dll
            code_size = file_size(binary_path)
            binary_size[binary_type] = code_size

    print_metrics(log_file, release)
