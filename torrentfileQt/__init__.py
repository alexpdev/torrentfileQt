#! /usr/bin/python3
# -*- coding: utf-8 -*-

##############################################################################
# Copyright 2020 AlexPDev
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
##############################################################################
"""Init module for TorrentfileQt project."""

import sys
import ctypes

import torrentfile

from torrentfileQt.version import __version__
from torrentfileQt.window import Application, Window, alt_start, start

myappid = f'TorrentfileQt.{__version__}'
if sys.platform == 'win32':
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

__author__ = "alexpdev"
__all__ = ["Application", "Window", "alt_start", "start", "__version__"]
