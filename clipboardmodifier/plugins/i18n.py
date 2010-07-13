#!/usr/bin/env python
# -*- encoding: latin1 -*-
#
# Copyright 2008 Scott Kirkwood

from _plugin import ClipboardPlugin, TestPlugin
import re
import wx

def create_plugin():
  return I18n()

class I18n(ClipboardPlugin):
  def __init__(self):
    ClipboardPlugin.__init__(self)
    
  def name(self):
    return 'Internaltionaliztion->I18n'
    
  def description(self):
    return 'Convert text like Internaltionaliztion to I18n'
    
  def convert(self, text):
    """Convert to abcdef to anf.
      
    Returns: Text
    """
    words = re.split(r'\s+', text)
    new_words = []
    for word in words:
      if len(word) > 5:
        word = word[0] + str(len(word) - 2) + word[-1]
      new_words.append(word)
    new_text = ' '.join(new_words)
    return self._ret_result("Converted", True, new_text)

class TestRot13(TestPlugin):
  def setUp(self):
    self.instance = I18n()
    
  def test_good(self):
    good_samples = [
      (u'localization', 'l10n'), 
      (u'europeanization', 'e13n'), 
      (u'japanization', 'j10n'), 
      (u'globalization', 'g11n'), 
      (u'canonicalization', 'c14n'),
      (u'normalization', 'n11n'),
      (u'localization', 'l10n'), 
      (u'europeanization', 'e13n'), 
      (u'japanization', 'j10n'), 
      (u'globalization', 'g11n'), 
      (u'canonicalization', 'c14n'),
      (u'normalization', 'n11n'),
      (u'globalization normalization', 'g11n n11n'),
      (u'scott kirkwood', 'scott k6d'),
    ]
    self.verify_good_samples(good_samples, "Converted")
    
if __name__ == "__main__":
  import unittest
  unittest.main()
