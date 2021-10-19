import os
import pytest
from PyQt6.QtWidgets import QApplication, QMainWindow, QStatusBar

from tests.context import testdata, testtorrent, testmeta, rmpath
from torrentfileGUI.window import alt_start, TabWidget

@pytest.fixture(scope="module")
def wind():
    window, app = alt_start()
    yield window
    app.quit()

@pytest.fixture(scope="module")
def tmeta():
    meta = testmeta()
    yield meta
    del meta

@pytest.fixture(scope="module")
def tdata():
    root = testdata()
    yield root
    rmpath(root)

@pytest.fixture(scope="module")
def ttorrent():
    path = testtorrent()
    yield path
    rmpath(path)

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

def test_info_tab_select(wind, ttorrent):
    infotab = wind.central.infoWidget
    button = infotab.selectButton
    button.selectTorrent(files=[ttorrent])
    assert infotab.nameEdit.text() != ""

def test_create_tab(wind, tdata):
    createtab = wind.central.createWidget
    button = createtab.browse_dir_button
    button.browse(path=tdata)
    torrentfile = tdata + ".test.torrent"
    outbutton = createtab.output_button
    outbutton.output(outpath=torrentfile)
    createtab.announce_input.setPlainText("announce.com")
    createtab.comment_input.setText("comment")
    createtab.private.click()
    submit = createtab.submit_button
    submit.click()
    assert os.path.exists(torrentfile)
