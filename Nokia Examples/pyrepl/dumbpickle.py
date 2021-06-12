# A really dumb pickle replacement, that converts the given object into a
# string with the repr function. Only objects that support repr and
# for which eval(repr(a))==a holds are accepted.
#
# Copyright (c) 2005 Nokia Corporation
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


def dump(obj, file, protocol=None, bin=None):
    file.write(dumps(obj,protocol,bin))

def dumps(obj, protocol=None, bin=None):
    if protocol or bin:
        raise "Arguments protocol and bin not implemented."
    objstr=repr(obj)
    # check that the object can be unpickled properly
    if eval(objstr)!=obj:
        raise "Sorry, dumbpickle can't pickle this object because "+\
              "eval(repr(obj))!=obj."
    return objstr

def load(file):
    return loads(' '.join(file.readlines()))

def loads(string):
    return eval(string)
    
