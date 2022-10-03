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
"""Module for style manager."""

import os
from copy import deepcopy
from pathlib import Path

from PySide6.QtCore import QObject, Signal
from PySide6.QtWidgets import QApplication, QFileDialog


class StyleManager(QObject):
    """Manage QStyleSheets for the app."""

    applyTheme = Signal(str)

    def __init__(self, themes):
        """Initialize styleManager class."""
        super().__init__()
        self.themes = themes
        self.parser = QssParser()
        self.current = None
        self.applyTheme.connect(self.set_app_theme)

    @staticmethod
    def set_app_theme(theme):
        """Set the current stylesheet."""
        app = QApplication.instance()
        app.set_new_theme(theme)

    def setTheme(self, theme: str):
        """
        Set the current QStyleSheet theme.

        Parameters
        ----------
        theme : str
            the qss formating string to apply as the theme.
        """
        self.applyTheme.emit(theme)

    def set_theme_from_title(self, title: str):
        """
        Set the theme from it's key in the theme dict.

        Parameters
        ----------
        title : str
            The key corresponding the the theme in the dict.
        """
        theme = self.themes[title]
        self.setTheme(theme)

    @staticmethod
    def _create_ssheet(sheets: list) -> str:
        """
        Update the sheet with data from table.

        Parameters
        ----------
        sheets : list
            list of all of the styles for a theme

        Returns
        -------
        dict
            the changed sheet
        """
        ssheet = ""
        for row in sheets:
            for k, v in row.items():
                if not k or not v:
                    continue  # pragma: nocover
                ssheet += k + " {\n"
                for key, val in v.items():
                    ssheet += "    " + key + ": " + val + ";\n"
                ssheet += "}\n"
        return ssheet

    def increase_font_size(self):
        """Increase the widgets font size."""
        self._adjust_font(1)

    def decrease_font_size(self):
        """Decrease the widgets font size."""
        self._adjust_font(-1)

    def _adjust_font(self, amount: int):
        """
        Adjust font size for all widgets.

        Parameters
        ----------
        amount: int
            the amount to adjust the font by.
        """
        widgets = self.parser.parse(self.current)
        for row in widgets:
            for _, value in row.items():
                if "font-size" in value:
                    val = value["font-size"]
                    number = int("".join([i for i in val if i.isdigit()]))
                    if 24 > number + amount > 0:
                        value["font-size"] = f"{number + amount}pt"
        theme = self._create_ssheet(widgets)
        self.applyTheme.emit(theme)


class QssParser:
    """Qt Style Sheet Parser."""

    def __init__(self):
        """Initialize and construct the qss parser object."""
        self.collection = []
        self.line_num = 0
        self.lines = []
        self.result = {}
        self.total = len(self.lines)

    def parse(self, sheet: str) -> dict:
        """
        Parse the provided qss sheet.

        Parameters
        ----------
        sheet : str
            Style sheet to parse.

        Returns
        -------
        dict
            collection of stylesheet strings
        """
        self.lines = sheet.split("\n")
        self.line_num = 0
        self.total = len(self.lines)
        self._parse_qss()
        return self.collection

    @property
    def current(self):
        """
        Return the current line.

        Returns
        -------
        str
            The current line
        """
        return self.lines[self.line_num]

    def _skipcomment(self):
        """Skip all lines until parser reaches the end comment token."""
        while "*/" not in self.current:
            self.line_num += 1
        self.line_num += 1

    def _add_widgets(self, widgets: str, props: dict):
        """
        Add widgets to the the master collection.

        Parameters
        ----------
        widgets : str
            The widgets name
        props : dict
            the property names and values
        """
        widget_str = "".join(widgets)
        widgets = widget_str.split(",")
        for widget in widgets:
            self.collection.append({widget.strip(): deepcopy(props)})

    @staticmethod
    def _serialize_prop(line: str) -> dict:
        """
        Normalize property string into name and value.

        Parameters
        ----------
        line : str
            the current line

        Returns
        -------
        dict
            the key,value pair of the normalized results
        """
        try:
            group = line.split(":")
            key, val = group[0].strip(), ":".join(group[1:]).strip()
            if val.endswith(";"):
                val = val[:-1]
            return {key: val}
        except IndexError:  # pragma: nocover
            return None

    def _parse_qss(self):
        """Parse the content of the qss file one line at a time."""
        inblock = False
        widgets, props = [], {}
        while self.line_num < self.total:
            if self.current == "":
                self.line_num += 1
                continue
            if "/*" in self.current:
                self._skipcomment()
                continue
            if "{" in self.current:
                sblock = self.current.index("{")
                widgets.append(self.current[:sblock])
                if "}" in self.current:
                    eblock = self.current.index("}")
                    prop = self.current[sblock:eblock]
                    prop = self._serialize_prop(prop)
                    if prop:
                        props.update(prop)
                    self._add_widgets(widgets, props)
                    widgets, props = [], {}
                    self.line_num += 1
                    continue
                self.line_num += 1
                inblock = True
                continue
            if "}" in self.current:
                inblock = False
                self._add_widgets(widgets, props)
                self.line_num += 1
                widgets, props = [], {}
                continue
            if inblock:
                parts = []
                while ";" not in self.current:
                    parts.append(self.current.strip())
                    self.line_num += 1
                parts.append(self.current.strip())
                prop = self._serialize_prop(" ".join(parts))
                if prop:
                    props.update(prop)
                self.line_num += 1
                continue
            widgets.append(self.current)
            self.line_num += 1

    def _compile(self):
        """Gather and group all results into one dictionary."""
        for row in self.collection:
            self.result.update(row)


def get_icon(name: str) -> str:
    """
    Return the path to the icon referenced by name.

    Parameters
    ----------
    name : str
        filename without extension for the icon.

    Returns
    -------
    str
        path to appropriate icon image
    """
    parent = os.path.dirname(__file__)
    assets = os.path.join(parent, "assets")
    path = os.path.join(assets, name)
    return path if path.endswith(".png") else path + ".png"


def browse_folder(widget: object, folder: str = None) -> str:
    """
    Browse for folder performed when user presses button.

    Parameters
    ----------
    widget : QWidget
        The widget making the call.
    folder : str
        Optional testing path

    Returns
    -------
    str
        folder path
    """
    if not folder:
        folder = QFileDialog.getExistingDirectory(  # pragma: nocover
            parent=widget,
            dir=str(Path.home()),
            caption="Select Contents Folder...",
        )
    if folder:
        folder = os.path.normpath(folder)
    return folder


def clean_list(lst: list) -> list:
    """Remove empty values from the list."""
    return [item for item in lst if item]


def browse_files(widget: object, paths: list = None) -> list:
    """
    Browse for files action performed when user presses button.

    Parameters
    ----------
    widget : QWidget
        The widget making the call.
    paths : list
        list of path strings

    Returns
    -------
    list
        list of pathstrings
    """
    if not paths:
        paths = QFileDialog.getOpenFileName(  # pragma: nocover
            parent=widget,
            dir=str(Path.home()),
            caption="Select Contents File...",
        )
    if paths and paths[0]:
        paths = [os.path.normpath(i) for i in paths if i]
    return paths


def browse_torrent(widget: object, torrents: list = None) -> list:
    """
    Browse for torrent file performed when user presses button.

    Parameters
    ----------
    widget : QWidget
        The widget making the call.
    torrents : list
        list of path strings

    Returns
    -------
    list
        list of path strings
    """
    if not torrents:
        torrents = QFileDialog.getOpenFileName(  # pragma: nocover
            parent=widget,
            dir=str(Path.home()),
            caption="Select *.torrent File...",
        )
    if torrents and torrents[0]:
        torrents = [os.path.normpath(i) for i in torrents if i]
    return torrents


def torrent_filter(paths: tuple) -> list:
    """
    Filter non torrent files from the given tuple of paths.

    Parameters
    ----------
    paths : tuple
        path strings

    Returns
    -------
    list
        torrent file paths
    """
    torrents = []
    for path in paths:
        if os.path.isfile(path) and path.endswith(".torrent"):
            torrents.append(path)
    return torrents
