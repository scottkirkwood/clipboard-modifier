#!/usr/bin/env python
# -*- encoding: latin1 -*-
#
# Copyright 2007 Scott Kirkwood

from _plugin import ClipboardPlugin, TestPlugin
import copy
import re
import locale 
import urllib
import wx

def create_plugin():
  return FixNumbers()

class FixNumbers(ClipboardPlugin):
  def __init__(self):
    ClipboardPlugin.__init__(self)
    self.fromDecimalChar = '.'
    self.toDecimalChar = '.'
    
  def name(self):
    return 'Change $1,234.00 to 1234.00, for example.'
    
  def description(self):
    return 'Given the decimal character given below, strips all extra characters.'
    
  def convert(self, text):
    """Given the desired formatting it'll.
      
    Returns: Text
    """
    orig_loc = locale.localeconv
    struct = copy.copy(orig_loc())
    def my_localconf():
      return struct
    locale.localeconv = my_localconf
    struct['decimal_point'] = self.fromDecimalChar
    if self.fromDecimalChar == '.':
      notgoodchars = '[^0-9.-]'
    else:
      notgoodchars = '[^0-9,-]'
    text = re.sub(notgoodchars, '', text)
    f = locale.atof(text)
    struct['decimal_point'] = self.toDecimalChar
    new_text = locale.format('%f', f)
    locale.localeconv = orig_loc 

    return self._ret_result("Number fixed", True, new_text)

  def control_iter(self, dialog):
    rb = wx.RadioBox(dialog, -1, "From decimal char", wx.DefaultPosition, wx.DefaultSize,
        ['. (dot)', ', (comma)'], 2, wx.RA_SPECIFY_COLS)
    dialog.Bind(wx.EVT_RADIOBOX, self.EvtFromDecimalChar, rb)
    yield rb
    rb = wx.RadioBox(dialog, -1, "To decimal char", wx.DefaultPosition, wx.DefaultSize,
        ['. (dot)', ', (comma)'], 2, wx.RA_SPECIFY_COLS)
    dialog.Bind(wx.EVT_RADIOBOX, self.EvtToDecimalChar, rb)
    yield rb

  def EvtFromDecimalChar(self, event):
    if event.GetInt() == 0:
      self.fromDecimalChar = '.'
    else:
      self.fromDecimalChar = ','
    self.parent.ModifyText()

  def EvtToDecimalChar(self, event):
    if event.GetInt() == 0:
      self.toDecimalChar = '.'
    else:
      self.toDecimalChar = ','
    self.parent.ModifyText()

class TestFixNumbers(TestPlugin):
  def setUp(self):
    self.instance = FixNumbers()
    
  def test_comma_to_dot(self):
    self.instance.fromDecimalChar = ','
    self.instance.toDecimalChar = '.'
    good_samples = [
      ('12345,45', '12345.450000'),
      ('12.345,67', '12345.670000'),
      (' 12.345,67 ', '12345.670000'),
      ('(12.345,67)', '12345.670000'),
    ]
    self.verify_good_samples(good_samples, "Number fixed")

  def test_dot_to_comma(self):
    self.instance.fromDecimalChar = '.'
    self.instance.toDecimalChar = ','
    good_samples = [
      ('12345.45', '12345,450000'),
      ('12,345.67', '12345,670000'),
      (' 12,345.67 ', '12345,670000'),
      ('(12,345.67)', '12345,670000'),
    ]
    self.verify_good_samples(good_samples, "Number fixed")
  def test_dot_to_dot(self):
    self.instance.fromDecimalChar = '.'
    self.instance.toDecimalChar = '.'
    good_samples = [
      ('12345.45', '12345.450000'),
      ('12,345.67', '12345.670000'),
      (' 12,345.67 ', '12345.670000'),
      ('(12,345.67)', '12345.670000'),
    ]
    self.verify_good_samples(good_samples, "Number fixed")
    
if __name__ == "__main__":
  import unittest
  unittest.main()
