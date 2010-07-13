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
  return Rot13()

class Rot13(ClipboardPlugin):
  def __init__(self):
    ClipboardPlugin.__init__(self)
    
  def name(self):
    return 'ROT13 encode/decode.'
    
  def description(self):
    return 'Converts the text into or out of ROT13 encoding'
    
  def convert(self, text):
    """Convert to ROT13
      
    Returns: Text
    """
    new_text = text.encode('rot13')
    return self._ret_result("Converted", True, new_text)

class TestRot13(TestPlugin):
  def setUp(self):
    self.instance = Rot13()
    
  def test_good(self):
    good_samples = [
      (u'nop', 'abc'),
      (u'abc', 'nop'),
      (u'aha', 'nun'),
      (u'ant', 'nag'),
      (u'balk', 'onyx'),
      (u'bar', 'one'),
      (u'barf', 'ones'),
      (u'be', 'or'),
      (u'bin', 'ova'),
      (u'ebbs', 'roof'),
      (u'envy', 'rail'),
      (u'er', 're'),
      (u'errs', 'reef'),
      (u'flap', 'sync'),
      (u'fur', 'she'),
      (u'gel', 'try'),
      (u'gnat', 'tang'),
      (u'irk', 'vex'),
      (u'clerk', 'pyrex'),
      (u'purely', 'cheryl'),
      (u'PNG', 'CAT'),
      (u'SHA', 'FUN'),
      (u'furby', 'sheol'),
      (u'terra', 'green'),
      (u'what', 'jung'),
      (u'URL', 'HEY'),
      (u'Purpura', 'Chechen'),
      (u'SHONE', 'FUBAR'),
    ]
    self.verify_good_samples(good_samples, "Converted")
    
if __name__ == "__main__":
  import unittest
  unittest.main()
