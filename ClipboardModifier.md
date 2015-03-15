# Introduction #

Clipboard modifier is a simple yet flexible Python program to modify the text contents of the text part of the clipboard.

# Details #

By adding plugins you can create your own routines to modify the clipboard in ways that you require.

[Creating A Plugin](CreatingAPlugin.md) describes how to do this.

# Current List of Plugins #

  * PluginDoNothing - Don't modify the clipboard, the first and the default.
  * PluginToJava - Converts text into "text".  Multiple lines will be created by adding pluses at the beginning.  If the text already contains a double quote it is escaped.
  * PluginAmazonLink - Modify an URL to add your Amazon Associate ID
  * PluginTabToBars - Modify a spreadsheet so that it works in a Wiki.
  * PluginColsToCommaSep - Convert tab delimited columns into comma separated string values.
  * PluginForceToText - Remove the other clipboard types so that only type text exists.
  * PluginRunApp - Run a program like sort and pass the clipboard as stdin, and grab the new clipboard as standard out.
  * PluginShowPythonVar - Convert your text using a template. The default example converts "myvar" into "print "myvar = %s" % str(myvar)"
  * PluginText2Unicode - Convert Unicode text into it's \u0000 unicode value.
  * PluginUrl2Python - Take a complicated URL with parameters and convert it into an easier to read python representation.
  * PluginUrl2Text - Convert an url with %0a escaped characters to plain text.