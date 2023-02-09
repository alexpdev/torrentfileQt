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

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QIcon, QMouseEvent
from PySide6.QtWidgets import (QFileDialog, QGroupBox, QHBoxLayout, QLabel,
                               QPushButton, QVBoxLayout, QWidget)


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
    icon = path if path.endswith(".png") else path + ".png"
    return QIcon(icon)


def browse_folder(widget: object) -> str:
    """
    Browse for folder performed when user presses button.

    Parameters
    ----------
    widget : QWidget
        The widget making the call.

    Returns
    -------
    str
        folder path
    """
    folder = QFileDialog.getExistingDirectory(
        parent=widget,
        dir=str(Path.home()),
        caption="Select Folder",
    )
    if folder:
        folder = os.path.normpath(folder)
    return folder


def clean_list(lst: list) -> list:
    """Remove empty values from the list."""
    return [item for item in lst if item]  # pragma: nocover


def browse_files(widget: object) -> list:
    """
    Browse for files action performed when user presses button.

    Parameters
    ----------
    widget : QWidget
        The widget making the call.

    Returns
    -------
    list
        list of pathstrings
    """
    path, _ = QFileDialog.getOpenFileName(parent=widget,
                                          dir=str(Path.home()),
                                          caption="Select File")
    if not path:
        path = ""
    return os.path.normpath(path)


def browse_torrent(widget: object) -> list:
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
    torrents = QFileDialog.getOpenFileName(
        parent=widget,
        dir=str(Path.home()),
        caption="Select *.torrent File...",
        filter=("torrent (*.torrent);;Any (*.*)"),
    )
    if not torrents[0]:
        return None
    return torrents[0]


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


class DropGroupBox(QGroupBox):
    """Drag and drop class."""

    pathSelected = Signal(str)

    def __init__(self, parent: QWidget = None):
        """
        Create groupbox with buttons inside for dragging and dropping.

        Parameters
        ----------
        parent : QWidget, optional
            _description_, by default None
        """
        super().__init__(parent=parent)
        self.setProperty("DropGroupBox", True)
        self.setAcceptDrops(True)
        self.layout = QVBoxLayout(self)
        self._label = QLabel("")
        self._label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._path = None
        self.layout.addWidget(self._label)
        self.hlayout = QHBoxLayout()
        self.layout.addLayout(self.hlayout)

    def addButton(self, button: QPushButton):
        """Add a button widget to groupbox."""
        self.hlayout.addWidget(button)

    def setLabelText(self, text: str):
        """Set the label text."""
        self._label.setText(text)

    def setPath(self, path: str):
        """Set the path."""
        self._path = path
        path_obj = Path(path)
        if len(path_obj.parts) > 2:
            last_sect = path_obj.parts[-2:]
            self.setLabelText("..." + os.path.join(*last_sect))
        else:
            self.setLabelText(path)  # pragma: nocover

    def getPath(self) -> str:
        """Get the path."""
        return self._path

    def dragEnterEvent(self, event: QMouseEvent) -> bool:
        """Drag enter event for widget."""
        if event.mimeData().hasUrls:
            event.accept()
            return True
        return event.ignore()

    def dragMoveEvent(self, event: QMouseEvent) -> bool:
        """Drag Move Event for widgit."""
        if event.mimeData().hasUrls:
            event.accept()
            return True
        return event.ignore()

    def dropEvent(self, event: QMouseEvent) -> bool:
        """Drag drop event for widgit."""
        urls = event.mimeData().urls()
        path = urls[0].toLocalFile()
        if os.path.exists(path):
            path = os.path.normpath(path)
            self.setLabelText(path)
            self.pathSelected.emit(path)
            return True
        return False
