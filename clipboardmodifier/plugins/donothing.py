#!/usr/bin/env python
# -*- encoding: latin1 -*-
#
# Copyright 2007 Scott Kirkwood

from _plugin import ClipboardPlugin, TestPlugin
import re

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
