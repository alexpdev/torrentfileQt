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


class StyleManager:
    """Manage QStyleSheets for the app."""

    def __init__(self, themes, current, parent):
        """Initialize styleManager class."""
        self.themes = themes
        self.current = current
        self.app = parent
        self.parser = QssParser()
        self.setTheme("light")

    def setTheme(self, title):
        """Set the current QStyleSheet theme."""
        self.app.apply_theme(self.themes[title])

    def _create_ssheet(self, sheets=None) -> dict:
        """
        Update the sheet with data from table.

        Returns
        -------
        dict
            the changed sheet
        """
        ssheet = ""
        if not sheets:
            sheets = self.sheets
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

    def _adjust_font(self, amount):
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
                    number = int(''.join([i for i in val if i.isdigit()]))
                    if 24 > number + amount > 0:
                        value["font-size"] = f"{number + amount}pt"
        theme = self._create_ssheet(widgets)
        self.app.apply_theme(theme)



class QssParser:
    """Qt Style Sheet Parser."""

    def __init__(self):
        """Initialize and construct the qss parser object."""
        self.collection = []
        self.line_num = 0
        self.lines = []
        self.total = len(self.lines)

    def parse(self, sheet):
        """
        Parse the provided qss sheet.

        Parameters
        ----------
        path : str
            Style sheet to parse.
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
        """
        Skip all lines until parser reaches the end comment token.
        """
        while "*/" not in self.current:
            self.line_num += 1
        self.line_num += 1

    def _add_widgets(self, widgets, props):
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
    def _serialize_prop(line):
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
        """
        Parse the content of the qss file one line at a time.
        """
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
        """
        Gather and group all results into one dictionary.
        """
        for row in self.collection:
            self.result.update(row)


def get_icon(name):
    """
    Return the path to the icon referenced by name.

    Parameters
    ----------
    name : str
        filename without extension for the icon.
    """
    parent = os.path.dirname(__file__)
    assets = os.path.join(parent, "assets")
    path = os.path.join(assets, name + ".png")
    return path
