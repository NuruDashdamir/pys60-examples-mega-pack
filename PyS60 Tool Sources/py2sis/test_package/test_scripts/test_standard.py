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
import marshal, os
import random
from sys import ps1, ps2
import time as mytime
from time import time as current_time
from email import *
import encodings.aliases
import encodings
from difflib import get_close_matches as matched


class StandardModTest(unittest.TestCase):

    def __init__(self, methodName='runTest'):
        unittest.TestCase.__init__(self, methodName=methodName)

    def test_functionality(self):
        randid = random.randint(0, 20)
        if not randid in range(0, 20):
            self.fail("Broken")
        print "The current time is : ", mytime.clock()
        if mytime.daylight:
            self.fail("Broken")
        print "Current time is : ", current_time()
        print "The current working directory is ", os.getcwd()
        print "email testing : ", message_from_string("Hello!")
        norm_encoding = encodings.normalize_encoding('ISO8859-1')
        if norm_encoding != 'ISO8859_1':
            self.fail("encoding Broken")
        if ps1 in '>>> ' and ps2 in '... ':
            print "Working prompts"
        if marshal.version < 2:
            self.fail("marshal Broken")
        if 'apple' not in matched('appel', ['apple', 'peach', 'puppy']):
            self.fail("Broken")


def test_main():
    test.test_support.run_unittest(StandardModTest)

if __name__ == "__main__":
    test_main()
