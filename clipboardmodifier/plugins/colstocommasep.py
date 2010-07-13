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
  return ColsToCommas()

class ColsToCommas(ClipboardPlugin):
  def __init__(self):
    ClipboardPlugin.__init__(self)
    self.max_col_width = 30
    self.indent = ''

  def name(self):
    return 'Columns to Comma Separated'

  def description(self):
    return 'Turn columns into comma separated'

  def convert(self, text):
    """ Data that is in columns into something
    separated by quotes and commas
    
    Returns: Text
    """
    
    if len(text) == 0:
      return self._ret_result('Nothing to do', False)
    
    lines = text.split('\n')
    for rowIndex, line in enumerate(lines):
      lines[rowIndex] = [x.rstrip() for x in line.split('\t')]
    
    if len(lines) <= 1:
      return self._ret_result("Not likely a table", False)
    
    max_width = []
    for line in lines:
      for colIndex, col in enumerate(line):
        if colIndex >= len(max_width):
          max_width.append(0)
        curColLen = len(col)
        if curColLen > max_width[colIndex]:
          max_width[colIndex] = curColLen
        if max_width[colIndex] > self.max_col_width:
          max_width[colIndex] = self.max_col_width
    
    ret = []
    last_line = lines[-1]
    last_line_is_empty = True
    for col in last_line:
      if len(col) > 0:
        last_line_is_empty = False
        break
    if last_line_is_empty:
      lines = lines[:-1]
    
    for rowIndex, line in enumerate(lines):
      newLine = []
      for colIndex, col in enumerate(line):
        line = col.replace('"', '\\"')
        line = '"%s"' % (line)
        line = '%-*s' % (max_width[colIndex],  line)
        newLine.append(line)
      
      ret.append(self.indent + ', '.join(newLine))
      message = "Converted to strings with %d columns and %d lines" % (len(max_width), 
        len(ret))
    
    return self._ret_result(message, True, ',\n'.join(ret))

class TestColsToCommas(TestPlugin):
  def setUp(self):
    self.instance = ColsToCommas()
    
  def test_good(self):
    good_samples = [
      ('''One\tTwo\tThree
Col1\tCol2\tCol3''',
       '''"One", "Two", "Three",
"Col1", "Col2", "Col3"'''),
      ('''One\tTwo\tThree
Col1\tCol2\tCol3
''',  '''"One", "Two", "Three",
"Col1", "Col2", "Col3"'''),
      ('''On"e\tTwo\t"Three
Col1\tCol2\tCol3"''',
       '''"On\\"e", "Two", "\\"Three",
"Col1", "Col2", "Col3\\""'''),
    ]
    self.verify_good_samples(good_samples, "Converted")

  def test_bad(self):
    bad_samples = [
      "",
    ]
    self.verify_bad_samples(bad_samples)
    
if __name__ == "__main__":
  import unittest
  unittest.main()
