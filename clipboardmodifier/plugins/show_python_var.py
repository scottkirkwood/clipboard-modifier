#!/usr/bin/env python
# -*- encoding: latin1 -*-
#
# Copyright 2007 Scott Kirkwood

from _plugin import ClipboardPlugin, TestPlugin
import re
import wx

def create_plugin():
  return ShowPythonVar()

class ShowPythonVar(ClipboardPlugin):
  def __init__(self):
    ClipboardPlugin.__init__(self)
    self.reset()

  def reset(self):
    self.template = "print '%(var)s = %%s' %% str(%(var)s)" 

  def name(self):
    return 'Show python var'
    
  def description(self):
    return 'Makes "%s" into "%s"' % ('my_var', self.template % dict(var='my_var'))
    
  def convert(self, text):
    """ Convert some text using the expression given
      
    Returns: Text
    """

    failed = False
    try:
      text = self.template % dict(var=text)
    except ValueError:
      failed = True
    if failed:
      return False
    else:
      return self._ret_result("Converted", True, text)

  def control_iter(self, dialog):
    yield wx.StaticText(dialog, -1, 'Template:')
    text_ctrl = wx.TextCtrl(dialog, -1, self.template)
    yield text_ctrl
    dialog.Bind(wx.EVT_TEXT, self.ChangedTemplate, text_ctrl)

  def ChangedTemplate(self, event):
    self.template = event.GetString()
    failed = False
    try:
      text = self.template % dict(var='bob')
    except ValueError:
      failed = True
    if not failed:
      self.parent.ModifyText()

class TestShowPythonVar(TestPlugin):
  def setUp(self):
    self.instance = ShowPythonVar()
    
  def test_good(self):
    good_samples = [
      ("my_var",
       "print 'my_var = %s' % str(my_var)"),
    ]
    self.verify_good_samples(good_samples, "Converted")
    
if __name__ == "__main__":
  import unittest
  unittest.main()
