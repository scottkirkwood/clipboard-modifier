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

def create_plugin():
  return Url2Python()
  
class Url2Python(ClipboardPlugin):
  def __init__(self):
    ClipboardPlugin.__init__(self)

  def name(self):
    return 'Convert an URL into python'
  
  def description(self):
    return 'Convert an URL into pretty printed python'

  def convert(self, text):
    """ Convert an http://summary.com:1234/graphnav?duration=4d&expr=too-high
    to 'http://summary.com:1234/graphnvav?' + urllib.urlencode(dict(
           duration = '4d',
           expr = 'too-high,
       ))
    Returns text (url)
    """
    import cgi
    import urllib
    
    query, params = urllib.splitquery(text)
    if not query:
      return self._ret_result("Couldn't parse URL", False, "")
    if not params:
      return self._ret_result("Created python", True, query)
    
    args = cgi.parse_qsl(params)
    result = ["'%s?' + urllib.urlencode(dict(" % query]
    for key, value in args:
      result.append("  %s = '%s'," % (key, value))
    result.append('))')
    return self._ret_result("Created python", True, '\n'.join(result))

class TestUrl2Python(TestPlugin):
  def setUp(self):
    self.instance = Url2Python()
    
  def test_good(self):
    good_samples = [
      ("http://summary.com:1234/graphnav?duration=4d&expr=too-high%3Dglobal%3Aprr_qps%3Alimit_rate10m.summary%3Blower-limit%3Dglobal%3Aprr_qps%3Amin_rate10m.summary%3Bupper-limit%3Dglobal%3Aprr_qps%3Amax_rate10m.summary%3Btotal%3Dglobal%3Aprr_qps%3Arate10m.summary%3Bformat%28zone%3Aprr_qps%3Arate10m.summary%2C%22%25zone%25%22%29&title=Bob+Storage+Server+Activity+%5BKqps%5D&using=%28%242*0.001%29&grid=&with_0=lines+lw+3&with_1=lines+lw+3&with_2=lines+lw+3&with_3=lines+lw+3&key=left&refresh=60",
          '\n'.join([
            "'http://summary.com:1234/graphnav?' + urllib.urlencode(dict(",
            "  duration = '4d',",
            "  expr = 'too-high=global:prr_qps:limit_rate10m.summary;lower-limit=global:prr_qps:min_rate10m.summary;upper-limit=global:prr_qps:max_rate10m.summary;total=global:prr_qps:rate10m.summary;format(zone:prr_qps:rate10m.summary,\"%zone%\")',",
            "  title = 'Bob Storage Server Activity [Kqps]',",
            "  using = '($2*0.001)',",
            "  with_0 = 'lines lw 3',",
            "  with_1 = 'lines lw 3',",
            "  with_2 = 'lines lw 3',",
            "  with_3 = 'lines lw 3',",
            "  key = 'left',",
            "  refresh = '60',",
            "))"])
      ),
      ('bob',
       'bob'
      ),
    ]
    self.verify_good_samples(good_samples, "Created python")

  def test_bad(self):
    bad_samples = [
      '',
    ]
    self.verify_bad_samples(bad_samples)
    
if __name__ == "__main__":
  import unittest
  unittest.main()
