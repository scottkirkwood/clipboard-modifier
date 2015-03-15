# Introduction #

So you want to make your own plugin, good for you!

# Details #

  * Create you .py file inside the site-packages/clipboard\_modifier.../clipboardmodifier/plugins/ directory.
Just look for site-packages and clipboard\_modifier... and then the plugins subdirectory.
  * This .py file needs a top level function called "create\_plugin()" which returns an instance of a class which you define.
  * This class needs these methods:
    * name(self) - which returns the name that will be displayed in the dialog
    * description(self) - which returns a longer description which appears as a tooltip
    * convert(self, text) - which converts the text into other text.
    * message(self) - a message text from the last conversion
    * converted(self) - True or False if the last convert() worked or not.
    * It's easiest to `from _plugin import ClipboardPlugin, TestPlugin` and to derive your class from `ClipboardPlugin`.
    * Create some unit tests for your plugin by deriving from `TestPlugin` class.

# New Optional Features #

Some optional new methods you can define are:
  * control\_iter(self, dialog) which 'yields' an iterator of new wx.Windows objects (ex. wx.TextCtrl), for UI elements.
  * get\_state(self), in while you return a strings representing the current state of your plugin.
  * restore\_state(self, text).  The parent gives you a string to restore from (from a previous `get_state()` call).

Note: you may want to call your own methods responding to events from the window objects you created.  If you want the clipboard to be reparsed, call `self.parent.ModifyText()` after the user changed something.


The easiest way to do this is to look at the other examples in the plugins directory.