#!/usr/bin/env python
# -*- encoding: latin1 -*-
#
# Copyright 2010 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from _plugin import ClipboardPlugin, TestPlugin

def create_plugin():
  return DoNothing()

class DoNothing(ClipboardPlugin):
  def __init__(self):
    ClipboardPlugin.__init__(self)
    
  def name(self):
    return 'Leave clipboard alone'
    
  def description(self):
    return 'Leaves your clipboard intact'

  def message(self):
    return ''
  
  def converted(self):
    return False
  
  def convert(self, text):
    return ''


class TestDoNothing(TestPlugin):
  def setUp(self):
    self.instance = DoNothing()
    
  def test_good(self):
    samples = [
      "",
      "as;dfsdf",
    ]
    self.verify_bad_samples(samples)
    
if __name__ == "__main__":
  import unittest
  unittest.main()
