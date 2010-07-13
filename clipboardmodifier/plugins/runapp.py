#!/usr/bin/env python
# -*- encoding: latin1 -*-
#
# Copyright 2010 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from _plugin import ClipboardPlugin, TestPlugin
import subprocess
import wx

def create_plugin():
  return RunApp()

class RunApp(ClipboardPlugin):
  def __init__(self):
    ClipboardPlugin.__init__(self)
    self.application = "sort"
    self.arguments = "-n"
    
  def name(self):
    return 'Run a program'
    
  def description(self):
    return 'Run a program that accepts a stream from stdin and returns a stream in stdout'
    
  def convert(self, text):
    """ Convert the program by streaming to and from the application
      
    Returns: Text
    """
    args = self.application + ' ' + self.arguments
    p = subprocess.Popen(args, stdin=subprocess.PIPE,   
        stdout=subprocess.PIPE, close_fds=True, shell=True)
    pinput = p.stdin
    output = p.stdout
    pinput.write(text)
    pinput.close()
    ret = []
    for line in output:
      ret.append(line)
    return self._ret_result("Converted", True, ''.join(ret))

  def control_iter(self, dialog):
    yield wx.StaticText(dialog, -1, "Program")
    text_ctrl = wx.TextCtrl(dialog, -1, self.application)
    dialog.Bind(wx.EVT_TEXT, self.ApplicationChanged, text_ctrl)
    yield text_ctrl
    text_ctrl = wx.TextCtrl(dialog, -1, self.arguments)
    dialog.Bind(wx.EVT_TEXT, self.ArgumentsChanged, text_ctrl)
    yield text_ctrl

  def ApplicationChanged(self, event):
    self.application = event.GetString()

  def ArgumentsChanged(self, event):
    self.arguments = event.GetString()

class TestRunApp(TestPlugin):
  def setUp(self):
    self.instance = RunApp()
    self.instance.application = 'sort'
    self.instance.arguments = '-n'
    
  def test_good(self):
    good_samples = [
      ("11\n2\n3\n",
       '2\n3\n11\n'),
    ]
    self.verify_good_samples(good_samples, "Converted")
    
if __name__ == "__main__":
  import unittest
  unittest.main()
