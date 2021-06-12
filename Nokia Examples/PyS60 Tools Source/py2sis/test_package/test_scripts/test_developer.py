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

import sys
sys.path.append('c:\\data\\python')
import unittest
import test.test_support
import e32
from e32dbm import open
import e32calendar as calendar
from logs import *
from e32 import inactivity, get_capabilities
from e32 import pys60_version_info as information
import logging.handlers


class DeveloperModTest(unittest.TestCase):

    def __init__(self, methodName='runTest'):
        unittest.TestCase.__init__(self, methodName=methodName)

    def test_functionality(self):
        try:
            tuple_of_capas = e32.get_capabilities()
            db = calendar.open()
            print "No of entries is ", len(db)
            print "The time since the user is inactive: ", inactivity()
            if len(information) != 5:
                self.fail("Broken")
            if not len(get_capabilities()):
                self.fail("Broken")
            print "The log of calls are: ", calls()
        except:
            self.fail("Something is broken")


def test_main():
    test.test_support.run_unittest(DeveloperModTest)

if __name__ == "__main__":
    test_main()
