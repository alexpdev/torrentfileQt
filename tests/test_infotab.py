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
import os

import pytest

from tests.context import Temp, build, fillfile, mktorrent, pathstruct, rmpath


@pytest.mark.parametrize("struct", pathstruct())
@pytest.mark.parametrize("hasher", Temp.hashers)
def test_info_tab_select1(struct, hasher):
    """Test Info tab select1."""
    path = build(struct)
    torrent = mktorrent(path, hasher)
    infotab = Temp.window.central.infoWidget
    Temp.app.processEvents()
    Temp.window.central.setCurrentWidget(infotab)
    button = infotab.selectButton
    button.selectTorrent(path=torrent)
    assert infotab.nameEdit.text() != ""  # nosec
    rmpath(path, torrent)


@pytest.mark.parametrize("size", list(range(16, 23)))
@pytest.mark.parametrize("ext", [".mp4", ".rar", ".m4a"])
@pytest.mark.parametrize("hasher", Temp.hashers)
def test_infotab_select2(size, hasher, ext):
    """Test getting info for single file torrent."""
    name = f"file{Temp.stamp()}{ext}"
    path = os.path.join(Temp.root, name)
    fillfile(path, size)
    torrent = hasher(path=path)
    del torrent.meta["created by"]
    del torrent.meta["creation date"]
    del torrent.meta["announce list"]
    outfile, _ = torrent.write()
    infotab = Temp.window.central.infoWidget
    Temp.app.processEvents()
    Temp.window.central.setCurrentWidget(infotab)
    button = infotab.selectButton
    button.selectTorrent(path=outfile)
    assert infotab.nameEdit.text() == name  # nosec
    rmpath(path, outfile)
