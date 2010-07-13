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
import re

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
