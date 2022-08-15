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
"""Module holding common functions."""



def increase_font_size(widget):
    """Increase the widgets font size."""
    font = widget.font()
    size = font.pointSize()
    font.setPointSize(size + 1)
    widget.setFont(font)


def decrease_font_size(widget):
    """Decrease the widgets font size."""
    font = widget.font()
    size = font.pointSize()
    font.setPointSize(size - 1)
    widget.setFont(font)
