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

from tests.context import tstdir3
import os
import pytest
from pathlib import Path

from PyQt6.QtWidgets import QApplication, QMainWindow, QStatusBar


from torrentfile import TorrentFile, TorrentFileV2, TorrentFileHybrid

from tests.context import tstdir, tstfile, tstdir2, rmpath
from torrentfileQt.window import alt_start, TabWidget
from torrentfileQt import menu
from torrentfileQt import qss


@pytest.fixture(scope="module")
def wind():
    window, app = alt_start()
    yield window
    app.quit()


@pytest.fixture(scope="module", params=[tstdir, tstdir2])
def tdir(request):
    root = request.param()
    return root


@pytest.fixture(scope="module", params=list(range(14, 28)))
def tfile(request):
    path = tstfile(val=request.param)
    return path


@pytest.fixture(
    scope="module", params=[TorrentFile, TorrentFileV2, TorrentFileHybrid]
)
def ttorrent1(tfile, request):
    path = tfile
    args = {
        "path": path,
        "private": 1,
        "announce": "tracker1.com",
        "comment": "this is a comment",
        "source": "Tracker",
    }
    torrent = request.param(**args)
    outfile, _ = torrent.write()
    return outfile


@pytest.fixture(
    scope="module", params=[TorrentFile, TorrentFileV2, TorrentFileHybrid]
)
def dtorrent1(tdir, request):
    path = tdir
    args = {
        "path": path,
        "private": 1,
        "announce": "tracker1.com",
        "comment": "this is a comment",
        "source": "Tracker",
    }
    torrent = request.param(**args)
    outfile, _ = torrent.write()
    return outfile


@pytest.fixture(
    scope="module", params=[TorrentFile, TorrentFileV2, TorrentFileHybrid]
)
def ttorrent2(tfile, request):
    path = tfile
    args = {"path": path}
    torrent = request.param(**args)
    outfile, _ = torrent.write()
    return outfile


@pytest.fixture(
    scope="module", params=[TorrentFile, TorrentFileV2, TorrentFileHybrid]
)
def dtorrent2(tdir, request):
    args = {"path": tdir}
    torrent = request.param(**args)
    outfile, _ = torrent.write()
    return outfile


def test_window1(wind):
    assert wind is not None


def test_window2(wind):
    assert isinstance(wind, QMainWindow)


def test_app1(wind):
    assert wind.app is not None


def test_app2(wind):
    assert isinstance(wind.app, QApplication)


def test_qss():
    assert qss


def test_window_menubar1(wind):
    assert wind.menubar is not None


def test_window_statusbar1(wind):
    assert wind.statusbar is not None


def test_window_statusbar2(wind):
    assert isinstance(wind.statusbar, QStatusBar)


def test_tab_widget(wind):
    tabwidget = wind.central
    assert isinstance(tabwidget, TabWidget)


def test_info_tab_select1(wind, ttorrent1):
    infotab = wind.central.infoWidget
    button = infotab.selectButton
    button.selectTorrent(files=[ttorrent1])
    assert infotab.nameEdit.text() != ""


def test_info_tab_select2(wind, ttorrent2):
    infotab = wind.central.infoWidget
    button = infotab.selectButton
    button.selectTorrent(files=[ttorrent2])
    assert infotab.nameEdit.text() != ""


def test_info_tab_dselect1(wind, dtorrent1):
    infotab = wind.central.infoWidget
    button = infotab.selectButton
    button.selectTorrent(files=[dtorrent1])
    assert infotab.nameEdit.text() != ""


def test_info_tab_dselect2(wind, dtorrent2):
    infotab = wind.central.infoWidget
    button = infotab.selectButton
    button.selectTorrent(files=[dtorrent2])
    assert infotab.nameEdit.text() != ""


def test_create_tab_dir(tdir, wind):
    root = tdir
    createtab = wind.central.createWidget
    button = createtab.browse_dir_button
    button.browse(root)
    torfile = root + ".test.torrent"
    outbutton = createtab.output_button
    outbutton.output(outpath=torfile)
    createtab.announce_input.setPlainText("announce.com")
    createtab.comment_input.setText("comment")
    createtab.private.click()
    submit = createtab.submit_button
    submit.click()
    assert os.path.exists(torfile)
    rmpath(torfile)


def test_create_tab_file(wind, tfile):
    createtab = wind.central.createWidget
    button = createtab.browse_file_button
    button.browse(tfile)
    torfile = tfile + ".test.torrent"
    outbutton = createtab.output_button
    outbutton.output(outpath=torfile)
    createtab.announce_input.setPlainText("announce.com")
    createtab.comment_input.setText("comment")
    createtab.private.click()
    submit = createtab.submit_button
    submit.click()
    assert os.path.exists(torfile)
    rmpath(torfile)


def test_create_tab_file_v2(wind, tfile):
    createtab = wind.central.createWidget
    button = createtab.browse_file_button
    createtab.v2button.click()
    button.browse(tfile)
    torfile = tfile + ".test.torrent"
    outbutton = createtab.output_button
    outbutton.output(outpath=torfile)
    createtab.announce_input.setPlainText("announce.com")
    createtab.comment_input.setText("comment")
    createtab.private.click()
    submit = createtab.submit_button
    submit.click()
    assert os.path.exists(torfile)


def test_create_tab_file_hybrid(wind, tfile):
    createtab = wind.central.createWidget
    button = createtab.browse_file_button
    createtab.hybridbutton.click()
    button.browse(path=tfile)
    torfile = tfile + ".test.torrent"
    outbutton = createtab.output_button
    outbutton.output(outpath=torfile)
    createtab.announce_input.setPlainText("announce.com")
    createtab.comment_input.setText("comment")
    createtab.private.click()
    submit = createtab.submit_button
    submit.click()
    assert os.path.exists(torfile)


def test_check_tab(wind, ttorrent1):
    checktab = wind.central.checkWidget
    testdir = os.path.dirname(ttorrent1)
    checktab.browseButton1.browse(path=testdir)
    checktab.browseButton2.browse(path=testdir)
    assert checktab.searchInput.text() != ""


def test_check_tab2(wind, ttorrent2):
    checktab = wind.central.checkWidget
    testdir = os.path.dirname(ttorrent2)
    checktab.browseButton1.browse(path=testdir)
    checktab.browseButton2.browse(path=testdir)
    assert checktab.fileInput.text() != ""


def test_check_dtab(wind, dtorrent1):
    checktab = wind.central.checkWidget
    testdir = os.path.dirname(dtorrent1)
    checktab.browseButton1.browse(path=testdir)
    checktab.browseButton2.browse(path=testdir)
    assert checktab.searchInput.text() != ""


def test_check_dtab2(wind, dtorrent2):
    checktab = wind.central.checkWidget
    testdir = os.path.dirname(dtorrent2)
    checktab.browseButton1.browse(path=testdir)
    checktab.browseButton2.browse(path=testdir)
    assert checktab.fileInput.text() != ""


def test_check_tab4(wind):
    checktab = wind.central.checkWidget
    tree_widget = checktab.treeWidget
    assert tree_widget.invisibleRootItem() is not None


def test_check_2tab5(wind, ttorrent2):
    checktab = wind.central.checkWidget
    metafile = ttorrent2
    contents = os.path.splitext(ttorrent2)[0]
    checktab.fileInput.setText(metafile)
    checktab.searchInput.setText(contents)
    checktab.checkButton.click()
    assert checktab.textEdit.toPlainText() != ""


def test_check_1tab5(wind, ttorrent1):
    checktab = wind.central.checkWidget
    metafile = ttorrent1
    contents = os.path.splitext(ttorrent1)[0]
    checktab.fileInput.setText(metafile)
    checktab.searchInput.setText(contents)
    checktab.checkButton.click()
    assert checktab.treeWidget.topLevelItemCount() > 0


def test_check_d2tab5(wind, dtorrent2):
    checktab = wind.central.checkWidget
    metafile = dtorrent2
    contents = os.path.splitext(dtorrent2)[0]
    checktab.fileInput.setText(metafile)
    checktab.searchInput.setText(contents)
    checktab.checkButton.click()
    assert checktab.treeWidget.topLevelItemCount() > 0


def test_check_tab5(wind, dtorrent1):
    checktab = wind.central.checkWidget
    metafile = dtorrent1
    contents = os.path.splitext(dtorrent1)[0]
    checktab.fileInput.setText(metafile)
    checktab.searchInput.setText(contents)
    checktab.checkButton.click()
    assert checktab.treeWidget.topLevelItemCount() > 0


def test_export_menu(wind, ttorrent2):
    infotab = wind.central.infoWidget
    button = infotab.selectButton
    button.selectTorrent(files=[ttorrent2])
    path = os.path.abspath("./tests/testfile.txt")
    wind.menubar.export(path=path)
    assert os.path.exists(path)
    rmpath(path)


@pytest.fixture
def wind2():
    window, app = alt_start()
    yield window
    app.quit()


@pytest.fixture
def tdir3():
    path = tstdir3()
    return path


@pytest.fixture(params=[TorrentFile, TorrentFileV2, TorrentFileHybrid])
def dtorrent1(tdir3, request):
    path = tdir3
    args = {
        "path": path,
        "private": 1,
        "announce": "tracker1.com",
        "comment": "this is a comment",
        "source": "Tracker",
    }
    torrent = request.param(**args)
    outfile, _ = torrent.write()
    return outfile


def test_missing_files_check(dtorrent1, wind):
    checktab = wind.central.checkWidget
    metafile = dtorrent1
    contents = os.path.splitext(dtorrent1)[0]
    dir1 = Path(contents) / "dir1"
    for item in dir1.iterdir():
        if item.is_file():
            os.remove(item)
    checktab.fileInput.setText(metafile)
    checktab.searchInput.setText(contents)
    checktab.checkButton.click()
    assert checktab.treeWidget.topLevelItemCount() > 0
