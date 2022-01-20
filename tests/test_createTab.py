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

from tests import dir1, dir2, rmpath, tempfile, wind


def test_rmpath():
    """Test the rmpath function."""
    fake = "./ajdiednvikjdod"
    rmpath(fake)
    assert not os.path.exists(fake)


def test_fixtures():
    """Test fixtures."""
    assert dir1 and dir2 and tempfile and wind


def test_create_with_hasher1(dir2, wind):
    """Test the radio buttons on create tab v1 hasher."""
    window, app = wind
    metafile = dir2 + ".torrent"
    creator = window.central.createWidget
    creator.window.central.setCurrentWidget(creator)
    app.processEvents()
    creator.path_input.clear()
    creator.path_input.setText(dir2)
    creator.output_input.clear()
    creator.output_input.setText(metafile)
    creator.v1button.setChecked(True)
    creator.piece_length.setCurrentIndex(2)
    creator.submit_button.click()
    creator.submit_button.join()
    assert os.path.exists(metafile)
    rmpath(metafile)


def test_create_tab_browse(dir2, wind):
    """Test Info tab select1."""
    window, app = wind
    path = dir2
    createtab = window.central.createWidget
    createtab.window.central.setCurrentWidget(createtab)
    app.processEvents()
    button = createtab.browse_file_button
    button.browse(path=path)
    createtab.comment_input.setText("Some Text")
    createtab.source_input.setText("Some Source")
    assert createtab.path_input.text() == path


def test_create_tab_dir(dir2, wind):
    """Test create tab with folder."""
    window, app = wind
    path = dir2
    root = path
    createtab = window.central.createWidget
    button = createtab.browse_dir_button
    window.central.setCurrentWidget(createtab)
    app.processEvents()
    button.browse(path=root)
    torfile = root + ".test.torrent"
    outbutton = createtab.output_button
    outbutton.output(outpath=torfile)
    createtab.announce_input.setPlainText("announce.com")
    createtab.comment_input.setText("comment")
    createtab.private.click()
    submit = createtab.submit_button
    submit.click()
    submit.join()
    assert os.path.exists(torfile)
    rmpath(torfile)


@pytest.mark.parametrize(
    "field",
    [
        "announce",
        "announce-list",
        "source",
        "private",
        "comment",
        "piece length",
    ],
)
def test_create_tab_fields(dir2, field, wind):
    """Test create tab with folder."""
    window, app = wind
    path = dir2
    root = path
    createtab = window.central.createWidget
    button = createtab.browse_dir_button
    button.browse(path=root)
    createtab.window.central.setCurrentWidget(createtab)
    app.processEvents()
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
    submit.join()
    result = pyben.load(torfile)
    assert field in result or field in result["info"]
    rmpath(torfile)


def test_sized_create(wind):
    """Test browse file button on create tab."""
    window, app = wind
    path = str(tempfile(exp=28))
    createtab = window.central.createWidget
    button = createtab.browse_file_button
    button.browse(path=path)
    app.processEvents()
    assert createtab.path_input.text() == path
