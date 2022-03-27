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

import pytest
from torrentfile import TorrentFile
from torrentfile import magnet

from tests import dir1, rmpath, tempfile, wind


@pytest.fixture(scope="module")
def torrent(dir1):
    """Creates torrent pytest fixture."""
    args = {
        "path": dir1,
        "source": "source",
        "announce": ["https://tracker1.com/announce"],
        "piece_length": "16",
        "comment": "some comment",
    }
    torrent = TorrentFile(**args)
    outfile, meta = torrent.write()
    yield outfile, meta
    rmpath(outfile)


def test_fixture():
    """Testing pytest fixtures."""
    assert [dir1, tempfile, wind]


def test_create_magnet(wind, torrent):
    """Test creating Magnet URI from a torrent file path."""
    window, app = wind
    outfile, _ = torrent
    tab = window.central.magnetWidget
    window.central.setCurrentWidget(tab)
    tab.metafile_input.setText(str(outfile))
    tab.submit_button.click()
    out = tab.output.text()
    app.processEvents()
    assert out == magnet(outfile)
