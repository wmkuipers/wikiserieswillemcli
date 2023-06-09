#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File: wikiserieswillemcliexceptions.py
#
# Copyright 2023 Willem Kuipers
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to
#  deal in the Software without restriction, including without limitation the
#  rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
#  sell copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
#  all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
#  FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
#  DEALINGS IN THE SOFTWARE.
#

"""
Custom exception code for wikiserieswillemcli.

.. _Google Python Style Guide:
   https://google.github.io/styleguide/pyguide.html

"""

__author__ = '''Willem Kuipers <willem@kuipers.co.uk>'''
__docformat__ = '''google'''
__date__ = '''01-05-2023'''
__copyright__ = '''Copyright 2023, Willem Kuipers'''
__credits__ = ["Willem Kuipers"]
__license__ = '''MIT'''
__maintainer__ = '''Willem Kuipers'''
__email__ = '''<willem@kuipers.co.uk>'''
__status__ = '''Development'''  # "Prototype", "Development", "Production".

class SeriesFolderAlreadyExistsError(FileExistsError):
    def __init__(self, path):
        self.path = path
        super().__init__(f"Path already exists: {self.path}")

class SeriesNotFoundError(FileExistsError):
   """Exception for a series not found on Wikipedia"""
   pass

class InvalidNameError(FileExistsError):
   """Exception for a series not found on Wikipedia"""
   pass
