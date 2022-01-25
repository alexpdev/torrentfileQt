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
import json
import os
from pathlib import Path

import pytest

from tests import wind, rmpath


@pytest.fixture(params=[1, 2, 3])
def profiles(request):
    """Pytest fixture for profiles."""
    root = Path(__file__).parent / "PROFILEDIR"
    profile_file = root / "profiles.json"
    if not os.path.exists(root):
        os.mkdir(root)
    with open(profile_file, "wt") as jsonfile:
        profile = {
            "example": {
                "version": request.param,
                "piece_length": 1048576,
                "source": "EXAMPLE",
                "private": True,
                "trackers": ["https://example.net/announce"],
                "web_seeds": [""],
            }
        }
        json.dump(profile, jsonfile)
    yield root, profile_file
    rmpath(root)


@pytest.fixture
def menubar_profiles(wind, profiles):
    """Pytest fixture for menubar profiles."""
    window, _ = wind
    menubar = window.menubar
    menubar.home, menubar.profiles = profiles
    menubar.add_profile_actions()
    return menubar, window, profiles


def test_wind():
    """Test pytest fixture for widnow."""
    assert wind


def test_menubar_profiles(menubar_profiles):
    """Test menubar profiles menu exists."""
    menubar, _, _ = menubar_profiles
    assert "example" in [i.name for i in menubar.profile_actions]


def test_menubar_profiles_actions(menubar_profiles):
    """Test menubar profiles actions."""
    menubar, window, profiles = menubar_profiles
    _, profile = profiles
    profs = json.load(open(profile))
    action = [i for i in menubar.profile_actions if i.name == "example"][0]
    action.action.trigger()
    tab = window.central.createWidget
    assert tab.source_input.text() == profs["example"]["source"]


def test_add_profile_with_profiles(menubar_profiles):
    """Test adding a profile."""
    menubar, window, profiles = menubar_profiles
    tab = window.central.createWidget
    tab.source_input.setText("SOURCE")
    tab.announce_input.setPlainText("https://announce.net")
    menubar.add_profile(name="test")
    _, profile = profiles
    profs = json.load(open(profile))
    assert "test" in profs


def test_add_profile_without_profiles(wind):
    """Test adding a profile."""
    window, _ = wind
    path = window.menubar.home
    alt = Path(__file__).parent / "alt"
    if os.path.exists(window.menubar.home):
        os.rename(path, alt)  # pragma: nocover
    tab = window.central.createWidget
    tab.source_input.setText("SOURCE")
    tab.announce_input.setPlainText("https://announce.net")
    window.menubar.add_profile(name="test")
    profiles = window.menubar.profiles
    profs = json.load(open(profiles))
    assert "test" in profs
    rmpath(path)
    if os.path.exists(alt):
        os.rename(alt, path)  # pragma: nocover
