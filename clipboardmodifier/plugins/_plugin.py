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

import unittest

class ClipboardPlugin:
  def __init__(self):
    self.last_message = ''
    self.was_converted = False

    # These will be filled in by the parent
    self.parent = None
    self.filename = None

  def message(self):
    """ Short message describing what happened

    Returns: String or empty string (not None)
    """
    return self.last_message

  def control_iter(self, unused_dialog):
    yield None

  def get_state(self):
    """Return your state as a string."""
    return ''

  def restore_state(self, string):
    """Restore the state given a string"""
    pass

  def converted(self):
    """ Was the last convet() call successfull?

    Returns: True/False
    """
    return self.was_converted

  def _ret_result(self, message, sucess, text=''):
    self.last_message = message
    self.was_converted = sucess
    return text

  def name(self):
    """ This is the name that appears in the dialog """
    pass

  def description(self):
    """ This is long description that shows up in tool tips """
    pass

  def convert(self, text):
    """ This is the function that does the actual convertion """

class TestPlugin(unittest.TestCase):
  def setUp(self):
    """ Setup self.instance here """
    pass

  def verify_good_samples(self, good_samples, expected_ok = None):
    """ Verify that an array of (intput, expected-output) match
    Ex
    """
    for good_sample, expected in good_samples:
      results = self.instance.convert(good_sample)
      self.assertTrue(self.instance.converted())
      if expected_ok != None:
        if not self.instance.message().startswith(expected_ok):
          self.fail("Expected: " + expected_ok + " but got " + self.instance.message())
      self.assertEquals(expected, results)

  def verify_bad_samples(self, bad_samples):
    for bad_sample in bad_samples:
      results = self.instance.convert(bad_sample)
      self.assertFalse(self.instance.converted())
      self.assertEquals('', results)

