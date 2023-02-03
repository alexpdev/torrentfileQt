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
"""Testing module for most of GUI."""
from PySide6.QtWidgets import QMainWindow

from tests import wind
from torrentfileQt import qss
from torrentfileQt.__main__ import main
from torrentfileQt.infoTab import denom

# def test_styleManager():
#     """Test style manager from utils module."""
#     themes = {
#         "test": """
# QWidget {
#     background-color: #000;
#     color: #0AF;
#     border-color: #F71;
#     border-width: 3px;
#     border-style: outset;
#     border-radius: 8px;
# }
# QLineEdit,
# QLabel {
#     font-size: 15pt;

# }
# /* this is a comment*/

# QCheckBox::indicator {
#     background-color: red;
#     margin: ;
# }

# /* this is a longer
# comment that spans two lines */

# QPushButton:pressed {
#     border-width:
#     3px;
#     border-style:
#     solid;
#     border-color:
#     #F71;
# }

# QPushButton:hover {color: #080;}
# /* some comment
# */
# QComboBox {
#     border: 12px solid pink;
# }"""
#     }
#     manager = StyleManager(themes)
#     manager.current = themes["test"]
#     collection = manager.parser.parse(themes["test"])
#     manager.parser._compile()
#     assert len(collection) > 1
