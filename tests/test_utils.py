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
"""Module for testing procedures on Bencode editor module."""

from tests import wind
from torrentfileQt import __main__, utils


def test_fix():
    """Fix pytest warnings."""
    assert wind


class MockClass:
    """Mock class for testing."""

    value = None

    @classmethod
    def getOpenFileName(cls, **_):
        """Mock method for testing."""
        return cls.value, None

    @classmethod
    def getExistingDirectory(cls, **_):
        """Mock method for testing."""
        return cls.value


utils.QFileDialog = MockClass


def test_themes(wind):
    """Test function for tesing utils."""
    wind.menubar.options_menu.actionDarkTheme.trigger()
    wind.menubar.options_menu.actionLightTheme.trigger()
    wind.titleBar.minimizeButton.click()
    wind.titleBar.minimizeButton.click()
    wind.titleBar.maximizeButton.click()
    wind.titleBar.maximizeButton.click()


def test_utils_browse_file():
    """Test function for tesing utils."""
    MockClass.value = "somevalue"
    assert utils.browse_files("obj") == MockClass.value


def test_utils_browse_folder():
    """Test function for tesing utils."""
    MockClass.value = "somevalue"
    assert utils.browse_folder("obj") == MockClass.value


def test_utils_browse_torrent():
    """Test function for tesing utils."""
    MockClass.value = "somevalue"
    assert utils.browse_torrent("obj") == MockClass.value


def test_utils_browse_no_file():
    """Test function for tesing utils."""
    MockClass.value = None
    assert utils.browse_files("obj") == "."


def test_utils_browse_no_folder():
    """Test function for tesing utils."""
    MockClass.value = None
    assert not utils.browse_folder("obj")


def test_utils_browse_no_torrent():
    """Test function for tesing utils."""
    MockClass.value = None
    assert not utils.browse_torrent("obj")


def test_qss_parser():
    """Test style manager from utils module."""
    themes = {
        "test": """
QWidget {
    background-color: #000;
    color: #0AF;
    border-color: #F71;
    border-width: 3px;
    border-style: outset;
    border-radius: 8px;
}
QLineEdit,
QLabel {
    font-size: 15pt;


}
/* this is a comment*/


QCheckBox::indicator {
    background-color: red;
    margin: ;
}

/* this is a longer
comment that spans two lines */

QPushButton:pressed {
    border-width:
    3px;
    border-style:
    solid;
    border-color:
    #F71;
}

QPushButton:hover {color: #080;}
/* some comment
*/
QComboBox {
    border: 12px solid pink;
}"""
    }
    parser = utils.QssParser()
    collection = parser.parse(themes["test"])
    parser._compile()
    assert len(collection) > 1
