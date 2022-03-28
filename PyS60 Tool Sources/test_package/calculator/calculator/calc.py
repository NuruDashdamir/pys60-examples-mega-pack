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

from odd_or_even import *


def sum(a,b,c):
    result = a + b + c
    return result


def subtract(a, b):
    if a > b:
        result = a - b
        return result
    else:
        print "First number should be greater than the second"


def multiply(a, b):
    return a * b


def divide(a, b):
    if b != 0:
        return a / b


def check_even(res):
    return is_even(res)
