#!/usr/bin/env python
# -*- encoding: latin1 -*-
#
# Copyright 2007 Scott Kirkwood

from _plugin import ClipboardPlugin, TestPlugin
import re

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
