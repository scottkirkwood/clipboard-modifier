#!/usr/bin/env python
# -*- encoding: latin1 -*-
#
# Copyright 2007 Scott Kirkwood

from _plugin import ClipboardPlugin, TestPlugin
import re

def create_plugin():
  return ForceToText()

class ForceToText(ClipboardPlugin):
  def __init__(self):
    ClipboardPlugin.__init__(self)
    self.plus_at_start = True
    
  def name(self):
    return 'Force clipboard text, only'
    
  def description(self):
    return 'Some applications support multiple clipboard format, force them to pick the text one'
    
  def convert(self, text):
    """ Convert Lines into Java strings
      
    Returns: Text
    """
    return self._ret_result("Forced to text", True, text)

class TestForceToText(TestPlugin):
  def setUp(self):
    self.instance = ForceToText()
    
  def test_good(self):
    good_samples = [
      ("String",
       'String'),
    ]
    self.verify_good_samples(good_samples, "Forced to text")
    
if __name__ == "__main__":
  import unittest
  unittest.main()
