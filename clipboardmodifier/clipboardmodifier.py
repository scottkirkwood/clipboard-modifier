#!/usr/bin/env python
# -*- encoding: latin1 -*-
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

__author__ = 'scott@forusers.com (Scott Kirkwood)'
__version__ = '0.2.1'

import ConfigParser
import optparse
import os
import plugins
import re
import sys
import wx

"""
Clipboard modifier is a wxPython app with a simple purpose.
When brought to the front, it'll modify the clipboard using a routine that you supply.
An example of this is talking the string "Hello" and putting it in quotes '"Hello'", which
becomes more interesting when you have several lines and some quotes within.
The program is exensible, any .py files found in the plugins subdirectory will get
loaded automatically. For each plugin we need a module level function called

Note to self:
Use the same naming conventions as wxPython in this file.
"""
class ClipboardModifierApp(wx.App):
  def init_vars(self):
    self.methods = []
    self.grabbedClipboard = ''
    self.sendClipboard = ''
    self.beforeTemplate = "From: %0d bytes"
    self.afterTemplate = "To: %0d bytes"
    self.unchanged_after = "Unchanged"
    self.config_name = '~/.clipboardmodifier'
    self.class_state = {}

  def OnInit(self):
    self.init_vars()
    dialog = wx.Frame(None, -1, "Clipboard Modifier")
    dialog.Show(True)
    self.SetTopWindow(dialog)
    self.FindModules()

    self.SetupControls(dialog)
    return True

  def SetupControls(self, dialog):
    self.vsizer = wx.BoxSizer(wx.VERTICAL)

    hsizer = wx.BoxSizer(wx.HORIZONTAL)
    self.dialog = dialog
    self.BeforeSize = wx.TextCtrl(dialog, -1, self.beforeTemplate % (0), size=(-1,20), style=wx.TE_READONLY)
    self.BeforeTooltip = wx.ToolTip("")
    self.BeforeTooltip.SetDelay(1)
    self.BeforeSize.SetToolTip(self.BeforeTooltip)
    hsizer.Add(self.BeforeSize, 1, wx.ALL, 5)

    self.AfterSize = wx.TextCtrl(dialog, -1, self.afterTemplate % (0), size=(-1, 20), style=wx.TE_READONLY)
    self.AfterTooltip = wx.ToolTip("")
    self.AfterTooltip.SetDelay(1)
    self.AfterSize.SetToolTip(self.AfterTooltip)
    hsizer.Add(self.AfterSize, 1, wx.ALL, 5)

    self.vsizer.Add(hsizer, 0, wx.ALL | wx.EXPAND, 5)

    # First one has this style, the remainder have a style of 0
    self.combo = wx.ComboBox(dialog, -1, style=wx.CB_DROPDOWN | wx.CB_READONLY)
    for class_instance in self.clipoard_methods:
      title = class_instance.name()
      self.combo.Append(title)

    self.Bind(wx.EVT_COMBOBOX, self.SetClassToUse, self.combo)
    self.vsizer.Add(self.combo, 0, wx.ALL | wx.EXPAND, 5)
    self.textDescription = wx.StaticText(dialog, -1, size=(-1, 40), style=wx.TE_READONLY)
    self.vsizer.Add(self.textDescription, 1, wx.ALL | wx.EXPAND, 10)
    #self.textDescription.Wrap(100)

    self.plugin_controls_sizer = wx.BoxSizer(wx.VERTICAL)
    self.vsizer.Add(self.plugin_controls_sizer, 0, wx.ALL | wx.EXPAND, 10)

    self.sb = dialog.CreateStatusBar()
    dialog.SetSizer(self.vsizer)
    self.combo.SetFocus()
    self.SetFromConfig(self.ReadConfig())

    wx.EVT_ACTIVATE(self, self.OnActivate)

  def ReadConfig(self):
    config = ConfigParser.ConfigParser()
    config.read(os.path.expanduser(self.config_name))
    return config;

  def SetFromConfig(self, config):
    num = 0
    if config.has_option('last', 'used'):
      num = config.getint('last', 'used')
    self.SetDefaultClass(num)

  def UpdateConfig(self):
    config = self.ReadConfig()
    if not config.has_section('last'):
      config.add_section('last')
    config.set('last', 'used', str(self.lastIndexUsed))
    fo = open(os.path.expanduser(self.config_name), 'w')
    config.write(fo)
    fo.close()

  def SetDefaultClass(self, index):
    self.lastIndexUsed = index
    self.class_to_use = self.clipoard_methods[index]
    self.combo.SetValue(self.class_to_use.name())
    self.SetClassInstance(self.clipoard_methods[index])

  def SetClassToUse(self, event):
    """User changed which class to use.

    Also forces a convert with the new class.
    """
    classTitle = event.GetString()
    for index, class_instance in enumerate(self.clipoard_methods):
      if class_instance.name() == classTitle:
        self.lastIndexUsed = index
        self.UpdateConfig()
        self.SetClassInstance(class_instance)
        return

  def SetClassInstance(self, class_instance):
    self.class_state[self.class_to_use.filename] = self.class_to_use.get_state()
    self.class_to_use = class_instance
    self.textDescription.SetLabel(class_instance.description())
    self.ModifyText()
    # This bit of magic resizes the StaticText() so that it wraps if it needs to.
    sizer = self.textDescription.GetContainingSizer()
    sizer.RecalcSizes()
    self.plugin_controls_sizer.DeleteWindows()
    for ctrl in self.class_to_use.control_iter(self.dialog):
      if ctrl:
        self.plugin_controls_sizer.Add(ctrl, 0, wx.ALL | wx.EXPAND, 0)
    self.dialog.Layout()
    if self.class_to_use.filename in self.class_state:
      self.class_to_use.restore_state(self.class_state[self.class_to_use.filename])

  def GrabClipboard(self):
    """ Grab the clipboard data """
    if wx.TheClipboard.Open():
      data = wx.TextDataObject()
      success = wx.TheClipboard.GetData(data)
      if success:
        self.grabbedClipboard = data.GetText()
      wx.TheClipboard.Close()

    return self.grabbedClipboard

  def UpdateClipboard(self, text):
    """ Overwrite the clipboard data """
    if wx.TheClipboard.Open():
      data = wx.TextDataObject(text)
      wx.TheClipboard.SetData(data)
      wx.TheClipboard.Close()
      return True
    return False

  def RunFunction(self, text, func):
    """ Run the function """
    results = func.convert(text)
    return func.message(), results

  def ModifyText(self):
    message = 'Ok'
    if len(self.grabbedClipboard) > 0:
      message, self.sendClipboard = self.RunFunction(self.grabbedClipboard, self.class_to_use)
    else:
      message = "No clipboard data"

    bytes_before = len(self.grabbedClipboard)
    bytes_after = len(self.sendClipboard)
    beforeMessage = self.beforeTemplate % (bytes_before)
    self.BeforeSize.SetValue(beforeMessage)
    afterMessage = ''
    if bytes_after == 0:
      afterMessage = self.unchanged_after
      self.AfterTooltip.SetTip(self.TrimTip(afterMessage))
    else:
      afterMessage = self.afterTemplate % (bytes_after)
      self.AfterTooltip.SetTip(self.TrimTip(self.sendClipboard))
    self.AfterSize.SetValue(afterMessage)

    self.BeforeTooltip.SetTip(self.TrimTip(self.grabbedClipboard))

    self.SetStatusBar(message)
    return message

  def SetStatusBar(self, message):
    self.sb.SetStatusText(message,0)
    wx.YieldIfNeeded()

  def TrimTip(self, text):
    """ Make sure the tip isn't too big """
    maxtip_size = 2048
    if len(text) > maxtip_size:
      return text[0:2048]+"..."
    return text

  def OnActivate(self, event):
    message = 'Ok'
    if event.GetActive():
      self.GrabClipboard()
      message = self.ModifyText()
    else:
      if len(self.sendClipboard) > 0:
        if not self.UpdateClipboard(self.sendClipboard):
          message = "Unable to update the clipboard"

    self.SetStatusBar(message)
    event.Skip()

  def FindModules(self):
    self.clipoard_methods = []

    pluginfiles = self._GetPluginFiles()
    self.import_plugin("plugins.donothing")
    for filename in pluginfiles:
      if filename.endswith('.py') \
          and not filename.startswith('_')  \
          and not filename == 'donothing.py':
        import_text = 'plugins.'  + filename.replace('.py', '')
        self.import_plugin(import_text)

  def import_plugin(self, import_text):
    print import_text
    try:
      __import__('clipboardmodifier.' + import_text)
    except:
      __import__(import_text) # This works when developing
    new_plugin = eval(import_text + '.create_plugin()')
    self.clipoard_methods.append(new_plugin)
    new_plugin.parent = self
    new_plugin.filename = import_text

  def _GetPluginFiles(self):
    plugindir = os.path.join(re.sub('__init__.py.?', '', plugins.__file__))
    ret = os.listdir(plugindir)
    return ret

class MyApp(wx.App):
  def OnInit(self):
    frame = ClipboardModifierApp(None, -1, 'Clipboard Modifier')
    frame.Show(True)
    self.SetTopWindow(frame)
    return True

def RunWxApp():
  app = ClipboardModifierApp(0)
  app.MainLoop()

def show_version():
  """Show the version number and author, used by help2man."""
  print 'Clipboard-modifier version %s.' % __version__
  print 'Written by %s' % __author__

if __name__ == '__main__':
  parser = optparse.OptionParser()
  parser.add_option('-v', '--version', dest='version', action='store_true',
                    help='Show version information and exit.')
  (options, args) = parser.parse_args()
  if options.version:
    show_version()
    sys.exit(0)

  RunWxApp()
