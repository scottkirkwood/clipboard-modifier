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
  return ToJava()

class ToJava(ClipboardPlugin):
  def __init__(self):
    ClipboardPlugin.__init__(self)
    self.plus_at_start = True
    
  def name(self):
    return 'Convert line(s) to Java Strings'
    
  def description(self):
    return 'Convert lines(s) into java strings escaping double quotes as needed.'
    
  def convert(self, text):
    """ Convert Lines into Java strings
      
    Returns: Text
    """
    
    if len(text) == 0:
      return self._ret_result('Nothing to do', False)
    
    lines = text.split('\n')
    
    last_line = lines[-1]
    last_line_is_empty = True
    for col in last_line:
      if len(col) > 0:
        last_line_is_empty = False
        break
    
    if last_line_is_empty:
      lines = lines[:-1]
    
    ret = []
    for rowIndex, line in enumerate(lines):
      newLine = line.replace('\\', '\\\\')
      newLine = newLine.replace('"', '\\"')
      ret.append('"%s"' % (newLine))
      
    message = "Put quotes around text" 
    return self._ret_result(message, True, '\n+'.join(ret))

class TestToJava(TestPlugin):
  def setUp(self):
    self.instance = ToJava()
    
  def test_good(self):
    good_samples = [
      ("String",
       '"String"'),
      (r'\n',
       r'"\\n"'),
      ('"Double quote"',
       '"\\"Double quote\\""'),
      ('''Two
Lines''',
       '''"Two"
+"Lines"'''),
    ]
    self.verify_good_samples(good_samples, "Put quotes around text")

  def test_bad(self):
    bad_samples = [
      "",
    ]
    self.verify_bad_samples(bad_samples)
    
if __name__ == "__main__":
  import unittest
  unittest.main()
