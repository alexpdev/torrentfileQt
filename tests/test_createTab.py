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

import pyben
import pytest

from tests.context import Temp, build, fillfile, pathstruct, rmpath


@pytest.mark.parametrize("size", list(range(16, 23)))
@pytest.mark.parametrize("struct", pathstruct())
def test_create_with_hasher1(size, struct):
    """Test the radio buttons on create tab v1 hasher."""
    path = build(struct, size=size)
    creator = Temp.window.central.createWidget
    creator.window.central.setCurrentWidget(creator)
    Temp.app.processEvents()
    creator.path_input.clear()
    creator.path_input.setText(path)
    creator.output_input.clear()
    creator.output_input.setText(path + ".torrent")
    creator.v1button.setChecked(True)
    creator.piece_length.setCurrentIndex(2)
    creator.submit_button.click()
    assert os.path.exists(path + ".torrent")  # nosec
    rmpath(path, path + ".torrent")


@pytest.mark.parametrize("size", list(range(16, 23)))
@pytest.mark.parametrize("struct", pathstruct())
def test_create_with_hasher2(size, struct):
    """Test the radio buttons on create tab v2 hasher."""
    creator = Temp.window.central.createWidget
    path = build(struct, size=size)
    creator.window.central.setCurrentWidget(creator)
    Temp.app.processEvents()
    creator.path_input.clear()
    creator.path_input.setText(path)
    creator.output_input.clear()
    creator.output_input.setText(path + ".torrent")
    creator.v2button.setChecked(True)
    creator.piece_length.setCurrentIndex(2)
    creator.submit_button.click()
    assert os.path.exists(path + ".torrent")  # nosec
    rmpath(path, path + ".torrent")


@pytest.mark.parametrize("size", list(range(16, 23)))
@pytest.mark.parametrize("struct", pathstruct())
def test_create_with_hybridhash(size, struct):
    """Test the radio buttons on create tab hybrid hasher."""
    creator = Temp.window.central.createWidget
    path = build(struct, size=size)
    creator.path_input.clear()
    creator.window.central.setCurrentWidget(creator)
    Temp.app.processEvents()
    creator.path_input.setText(path)
    creator.output_input.clear()
    creator.output_input.setText(path + ".torrent")
    creator.hybridbutton.setChecked(True)
    creator.piece_length.setCurrentIndex(2)
    creator.submit_button.click()
    assert os.path.exists(path + ".torrent")  # nosec
    rmpath(path, path + ".torrent")


@pytest.mark.parametrize("struct", pathstruct())
def test_create_tab_browse(struct):
    """Test Info tab select1."""
    path = build(struct)
    createtab = Temp.window.central.createWidget
    createtab.window.central.setCurrentWidget(createtab)
    Temp.app.processEvents()
    button = createtab.browse_file_button
    button.browse(path=path)
    createtab.comment_input.setText("Some Text")
    createtab.source_input.setText("Some Source")
    assert createtab.path_input.text() == path  # nosec
    rmpath(path)


@pytest.mark.parametrize("struct", pathstruct())
def test_create_tab_dir(struct):
    """Test create tab with folder."""
    path = build(struct)
    root = path
    createtab = Temp.window.central.createWidget
    button = createtab.browse_dir_button
    Temp.window.central.setCurrentWidget(createtab)
    Temp.app.processEvents()
    button.browse(path=root)
    torfile = root + ".test.torrent"
    outbutton = createtab.output_button
    outbutton.output(outpath=torfile)
    createtab.announce_input.setPlainText("announce.com")
    createtab.comment_input.setText("comment")
    createtab.private.click()
    submit = createtab.submit_button
    submit.click()
    assert os.path.exists(torfile)  # nosec
    rmpath(path, torfile)


@pytest.mark.parametrize(
    "field",
    [
        "announce",
        "announce list",
        "source",
        "private",
        "comment",
        "piece length",
    ],
)
@pytest.mark.parametrize("struct", pathstruct())
def test_create_tab_fields(struct, field):
    """Test create tab with folder."""
    path = build(struct)
    root = path
    createtab = Temp.window.central.createWidget
    button = createtab.browse_dir_button
    button.browse(path=root)
    createtab.window.central.setCurrentWidget(createtab)
    Temp.app.processEvents()
    torfile = root + ".test.torrent"
    outbutton = createtab.output_button
    outbutton.output(outpath=torfile)
    createtab.announce_input.setPlainText(
        "https://announce.com\nhttp://announce2.com\nhttp://announce4.com"
    )
    createtab.comment_input.setText("some comment")
    createtab.private.setChecked(True)
    createtab.source_input.setText("TestSource")
    submit = createtab.submit_button
    submit.click()
    result = pyben.load(torfile)
    assert field in result or field in result["info"]  # nosec
    rmpath(path, torfile)


def test_largefile_create():
    """Test browse file button on create tab."""
    name = f"file1{Temp.stamp()}"
    path = os.path.join(Temp.root, name)
    fillfile(path, 28)
    createtab = Temp.window.central.createWidget
    button = createtab.browse_file_button
    button.browse(path=path)
    Temp.app.processEvents()
    assert createtab.path_input.text() == path  # nosec


def test_largedir_create():
    """Test browse folder button on create tab."""
    name = f"dir{Temp.stamp()}"
    path = os.path.join(Temp.root, name)
    struct = [
        "dir1/file1.mkv",
        "dir2/file2.wav",
        "dir1/file3.deb",
        "file4.png",
    ]
    path = build(struct, 28)
    createtab = Temp.window.central.createWidget
    button = createtab.browse_dir_button
    button.browse(path=path)
    Temp.app.processEvents()
    assert os.path.exists(path)  # nosec
