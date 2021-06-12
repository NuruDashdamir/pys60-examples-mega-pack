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

import test.test_support
import unittest
# In case the module is not loaded, this test would be skipped
# - "No module named elemlist"
import elemlist


class ElemlistTest(unittest.TestCase):

    def __init__(self, methodName='runTest'):
        unittest.TestCase.__init__(self, methodName=methodName)
        self.car_accessor = 1
        self.cdr_accessor = 2
        self.cell = elemlist.cons(self.car_accessor, self.cdr_accessor)

    def test_cons(self):
        """Constructing"""
        self.failUnless(self.cell)

    def test_car(self):
        """Fetching car_accessor"""
        self.failUnlessEqual(elemlist.car(self.cell), self.car_accessor)

    def test_cdr(self):
        """Fetching cdr_accessor"""
        self.failUnlessEqual(elemlist.cdr(self.cell), self.cdr_accessor)


def test_main():
    test.test_support.run_unittest(ElemlistTest)

if __name__ == "__main__":
    test_main()
