import os

import pytest
from PyQt6.QtWidgets import QApplication, QMainWindow, QStatusBar
from torrentfile import TorrentFile, TorrentFileV2, TorrentFileHybrid

from tests.context import testdir, testfile, rmpath
from torrentfileQt.window import alt_start, TabWidget


@pytest.fixture(scope="module")
def wind():
    window, app = alt_start()
    yield window
    app.quit()


@pytest.fixture(scope="module")
def tdir(wind):
    root = testdir()
    yield root, wind
    rmpath(root)


@pytest.fixture(scope="module", params=list(range(14,28)))
def tfile(request):
    path = testfile(val=request.param)
    yield path


@pytest.fixture(scope="module", params=[TorrentFile, TorrentFileV2,
                                        TorrentFileHybrid])
def ttorrent1(tfile, request):
    path = tfile
    args = {
        "path": path,
        "private": 1,
        "announce": "tracker1.com",
        "comment": "this is a comment",
        "source": "Tracker",
        "announce_list": ["tracker2.com", "tracker3.com"]}
    torrent = request.param(**args)
    outfile, _ = torrent.write()
    yield outfile
    rmpath(outfile)


@pytest.fixture(scope="module", params=[TorrentFile, TorrentFileV2,
                                        TorrentFileHybrid])
def ttorrent2(tfile, request):
    path = tfile
    args = {"path": path}
    torrent = request.param(**args)
    outfile, _ = torrent.write()
    yield outfile
    rmpath(outfile)


def test_window1(wind):
    assert wind is not None


def test_window2(wind):
    assert isinstance(wind, QMainWindow)


def test_app1(wind):
    assert wind.app is not None


def test_app2(wind):
    assert isinstance(wind.app, QApplication)


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


def test_info_tab_select1(wind, ttorrent2):
    infotab = wind.central.infoWidget
    button = infotab.selectButton
    button.selectTorrent(files=[ttorrent2])
    assert infotab.nameEdit.text() != ""


def test_create_tab_dir(tdir):
    root, wind = tdir
    createtab = wind.central.createWidget
    button = createtab.browse_dir_button
    button.browse(path=root)
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
    rmpath(torfile)


def test_create_tab_file_v2(wind, tfile):
    createtab = wind.central.createWidget
    button = createtab.browse_file_button
    createtab.v2button.click()
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
    rmpath(torfile)


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
    rmpath(torfile)


def test_check_tab(wind, ttorrent1):
    checktab = wind.central.checkWidget
    testdir = os.path.dirname(ttorrent1)
    checktab.browseButton1.browse(path=testdir)
    checktab.browseButton2.browse(path=testdir)
    checktab.checkButton.click()
    assert checktab.fileInput.text() != ""


def test_check_tab(wind, ttorrent2):
    checktab = wind.central.checkWidget
    testdir = os.path.dirname(ttorrent2)
    checktab.browseButton1.browse(path=testdir)
    checktab.browseButton2.browse(path=testdir)
    checktab.checkButton.click()
    assert checktab.fileInput.text() != ""
