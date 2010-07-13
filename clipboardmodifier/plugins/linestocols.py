#!/usr/bin/env python
# -*- encoding: latin1 -*-
#
# Copyright 2007 Scott Kirkwood

from _plugin import ClipboardPlugin, TestPlugin
import re

def create_plugin():
  return LinesToCols()

class LinesToCols(ClipboardPlugin):
  def __init__(self):
    ClipboardPlugin.__init__(self)
    self.num_columns = 4

  def name(self):
    return 'Rows into columns/rows'

  def description(self):
    return 'Writely copies a table as a bunch of rows, make it into rows columns'

  def convert(self, text):
    """ Data that is in columns into something
    separated by quotes and commas
    
    Returns: Text
    """
    
    if len(text) == 0:
      return self._ret_result('Nothing to do', False)
    
    lines = text.split('\n')
    
    if len(lines) <= 1:
      return self._ret_result("Not likely a table", False)
    
    ret = []
    self.cur_row = []
    for line in lines:
      self._out_col(ret, line)
    self._append_row(ret)
    
    message = "Converted into %dx%d (row/cols)" % (len(ret), self.num_columns)
    return self._ret_result("Converted", True, '\n'.join(ret))
    
  def _out_col(self, ret, line):
    if len(self.cur_row) >= self.num_columns:
      self._append_row(ret)
    self.cur_row += line.lstrip().split('\t')
      
  def _append_row(self, ret):
      ret.append('\t'.join(self.cur_row))
      self.cur_row = []
    
class TestLinesToCols(TestPlugin):
  def setUp(self):
    self.instance = LinesToCols()
    
  def test_good(self):
    good_samples = [
      ("One\n\tTwo\n\tThree\nFour\nCol1\nCol2\nCol3\nCol4\n",
       "One\tTwo\tThree\tFour\nCol1\tCol2\tCol3\tCol4\n",),
      ("One\nTwo\nThree\nFour\nCol1\nCol2\nCol3\nCol4",
       "One\tTwo\tThree\tFour\nCol1\tCol2\tCol3\tCol4",),
      ("One\nTwo\nThree\nFour\nCol1\nCol2\nCol3",
       "One\tTwo\tThree\tFour\nCol1\tCol2\tCol3",),
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
