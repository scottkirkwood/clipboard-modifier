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
  return SearchReplace()

class SearchReplace(ClipboardPlugin):
  def __init__(self):
    self.fromRegex = r'([0-9]+)'
    self.toRegex = r'=\1'
    ClipboardPlugin.__init__(self)

  def reset(self):
    self.fromRegex = r'_'
    self.toRegex = r' '

  def name(self):
    return 'Generalized search and replace.'
    
  def description(self):
    return 'Search and replace with regular expressions.'
    
  def convert(self, text):
    """Conver the text using the regular expression.
      
    Returns: Text
    """
    re_compiled = None
    try:
      re_compiled = re.compile(self.fromRegex)
    except Exception, e:
      return False

    try:
      text = re_compiled.sub(self.toRegex, text)
    except Exception, e:
      return False
    return self._ret_result('Converted', True, text)

  def control_iter(self, dialog):
    yield wx.StaticText(dialog, -1, 'Regex:')

    regex_ctrl = wx.TextCtrl(dialog, -1, self.fromRegex)
    yield regex_ctrl
    dialog.Bind(wx.EVT_TEXT, self.ChangeRegex, regex_ctrl)

    yield wx.StaticText(dialog, -1, 'Replace:')
    to_ctrl = wx.TextCtrl(dialog, -1, self.toRegex)
    yield to_ctrl
    dialog.Bind(wx.EVT_TEXT, self.ChangeTo, to_ctrl)

  def ChangeRegex(self, event):
    self.fromRegex = event.GetString()
    self.parent.ModifyText()

  def ChangeTo(self, event):
    self.toRegex = event.GetString()
    self.parent.ModifyText()

  def get_state(self):
    return "{'from' : r'%s', 'to' : r'%s' }" % (self.fromRegex, self.toRegex)

  def restore_state(self, text):
    adict = eval(text)
    self.fromRegex = adict['from']
    self.toRegex = adict['to']


class TestSearchReplace(TestPlugin):
  def setUp(self):
    self.instance = SearchReplace()
    
  def testGroupedReplace(self):
    self.instance.fromRegex = r'([0-9])'
    self.instance.toRegex = r'_\1_'
    good_samples = [
      ('1', '_1_'),
      ('x9x', 'x_9_x'),
      ('xyz', 'xyz'),
    ]
    self.verify_good_samples(good_samples, "Converted")

  def testSimpleReplace(self):
    self.instance.fromRegex = r'[0-9]'
    self.instance.toRegex = r'_'
    good_samples = [
      ('1', '_'),
      ('x9x', 'x_x'),
      ('xyz', 'xyz'),
    ]
    self.verify_good_samples(good_samples, "Converted")

if __name__ == "__main__":
  import unittest
  unittest.main()
