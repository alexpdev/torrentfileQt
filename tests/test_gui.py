import pytest
from PyQt6.QtWidgets import QApplication, QMainWindow, QStatusBar

from torrentfileGUI.window import alt_start, TabWidget

@pytest.fixture(scope="module")
def wind():
    window, app = alt_start()
    yield window
    app.exec_()

@pytest.fixture(scope="module")
def app():
    _, app = alt_start()
    yield app
    app.exec_()

def test_window1(wind):
    assert wind is not None

def test_window2(wind):
    assert isinstance(wind, QMainWindow)

def test_app1(app):
    assert app is not None

def test_app2(app):
    assert isinstance(app, QApplication)

def test_window_menubar1(wind):
    assert wind.menubar is not None

def test_window_statusbar1(wind):
    assert wind.statusbar is not None

def test_window_statusbar2(wind):
    assert isinstance(wind.statusbar, QStatusBar)

def test_tab_widget(wind):
    tabwidget = wind.tabwidget
    assert isinstance(tabwidget, TabWidget)
