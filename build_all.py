#!/usr/bin/python
# -*- coding: utf-8 -*-
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

"""
Build everything for clipboard-modifier.

You'll need:
sudo apt-get install python-bdist
"""

from pybdist import pybdist
import optparse
import setup


def main():
  """Run the program, put here to make linter happy."""
  parser = optparse.OptionParser()
  pybdist.add_standard_options(parser)
  (options, unused_args) = parser.parse_args()

  if not pybdist.handle_standard_options(options, setup):
    print 'Doing nothing.  --help for commands.'

if __name__ == '__main__':
  main()
