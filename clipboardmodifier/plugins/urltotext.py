#!/usr/bin/env python
# -*- encoding: latin1 -*-
#
# Copyright 2007 Scott Kirkwood

from _plugin import ClipboardPlugin, TestPlugin
import urllib
import wx

def create_plugin():
  return UrlToText()

class UrlToText(ClipboardPlugin):
  def __init__(self):
    ClipboardPlugin.__init__(self)
    self.unquote = True
    
  def name(self):
    return 'Translate %0A to text'
    
  def description(self):
    return 'Hard to understand %0A into text'
    
  def convert(self, text):
    """Convert URL text into something readable.
      
    Returns: Text
    """
    if self.unquote:
      new_text = urllib.unquote_plus(text)
    else:
      new_text = urllib.quote_plus(text)
    return self._ret_result("Unquoted", True, new_text)

  def control_iter(self, dialog):
    cb = wx.CheckBox(dialog, -1, label='Unquote')
    cb.SetValue(self.unquote)
    dialog.Bind(wx.EVT_CHECKBOX, self.EvtCheckBox, cb)
    yield cb

  def EvtCheckBox(self, event):
    self.unquote = event.Checked()
    self.parent.ModifyText()

class TestUrl2Text(TestPlugin):
  def setUp(self):
    self.instance = UrlToText()
    
  def test_good(self):
    good_samples = [
      ("%2f%7Econnolly%2f",
       '/~connolly/'),
      ("hello+there",
       "hello there"),
    ]
    self.verify_good_samples(good_samples, "Unquoted")
    
if __name__ == "__main__":
  import unittest
  unittest.main()
