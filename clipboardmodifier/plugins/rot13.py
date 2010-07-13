#!/usr/bin/env python
# -*- encoding: latin1 -*-
#
# Copyright 2007 Scott Kirkwood

from _plugin import ClipboardPlugin, TestPlugin
import urllib
import wx

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
