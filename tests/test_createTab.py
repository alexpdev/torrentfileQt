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
"""Module for testing procedures on Check Tab."""

import os

import pytest

from tests.context import Temp, build, pathstruct, rmpath


@pytest.mark.parametrize("size", list(range(16, 23)))
@pytest.mark.parametrize("struct", pathstruct())
def test_create_with_hasher1(size, struct):
    """Test the radio buttons on create tab v1 hasher."""
    creator = Temp.window.central.createWidget
    Temp.window.central.setCurrentWidget(creator)
    path = build(struct, size=size)
    creator.path_input.clear()
    creator.path_input.setText(path)
    creator.output_input.clear()
    creator.output_input.setText(path + ".torrent")
    creator.v1button.setChecked(True)
    creator.piece_length.setCurrentIndex(2)
    creator.submit_button.click()
    assert os.path.exists(path + ".torrent")   # nosec
    rmpath([path, path + ".torrent"])


@pytest.mark.parametrize("size", list(range(16, 23)))
@pytest.mark.parametrize("struct", pathstruct())
def test_create_with_hasher2(size, struct):
    """Test the radio buttons on create tab v2 hasher."""
    creator = Temp.window.central.createWidget
    Temp.window.central.setCurrentWidget(creator)
    path = build(struct, size=size)
    creator.path_input.clear()
    creator.path_input.setText(path)
    creator.output_input.clear()
    creator.output_input.setText(path + ".torrent")
    creator.v2button.setChecked(True)
    creator.piece_length.setCurrentIndex(2)
    creator.submit_button.click()
    assert os.path.exists(path + ".torrent")   # nosec
    rmpath([path, path + ".torrent"])


@pytest.mark.parametrize("size", list(range(16, 23)))
@pytest.mark.parametrize("struct", pathstruct())
def test_create_with_hash1(size, struct):
    """Test the radio buttons on create tab hybrid hasher."""
    creator = Temp.window.central.createWidget
    Temp.window.central.setCurrentWidget(creator)
    path = build(struct, size=size)
    creator.path_input.clear()
    creator.path_input.setText(path)
    creator.output_input.clear()
    creator.output_input.setText(path + ".torrent")
    creator.hybridbutton.setChecked(True)
    creator.piece_length.setCurrentIndex(2)
    creator.submit_button.click()
    assert os.path.exists(path + ".torrent")      # nosec
    rmpath([path, path + ".torrent"])
