#!/usr/bin/env python
# -*- encoding: latin1 -*-
#
# Copyright 2007 Scott Kirkwood

from _plugin import ClipboardPlugin, TestPlugin
import urllib
import wx

def create_plugin():
  return Text2Unicode()

class Text2Unicode(ClipboardPlugin):
  def __init__(self):
    ClipboardPlugin.__init__(self)
    self.from_unicode = False
    
  def name(self):
    return 'Text to escaped unicode.'
    
  def description(self):
    return 'Foreign characters translated to unicode style escapes.'
    
  def convert(self, text):
    """Convert text into unicode
      
    Returns: Text
    """
    new_text = text.encode('unicode-escape', 'backslashreplace')
    return self._ret_result("Converted", True, new_text)

  def control_iter(self, dialog):
    cb = wx.CheckBox(dialog, -1, label='From Unicode')
    cb.SetValue(self.from_unicode)
    dialog.Bind(wx.EVT_CHECKBOX, self.EvtCheckBox, cb)
    yield cb

  def EvtCheckBox(self, event):
    self.from_unicode = event.Checked()
    self.parent.ModifyText()

class TestUrl2Text(TestPlugin):
  def setUp(self):
    self.instance = Text2Unicode()
    
  def test_good(self):
    good_samples = [
      (u'João',
      'Jo\\xe3o'),
    ]
    self.verify_good_samples(good_samples, "Converted")
    
if __name__ == "__main__":
  import unittest
  unittest.main()
