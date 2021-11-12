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
"""Module for testing procedures on context module."""

import os

from tests import context


def test_rmpath():
    """Test rmpath function."""
    temp = os.path.join(context.Temp.root, "rmpathfile")
    with open(temp, "wt") as fd:
        fd.write("10101")
    assert os.path.exists(temp)  # nosec
    context.rmpath(temp)
    assert not os.path.exists(temp)  # nosec


def test_fillfile():
    """Test fill file function."""
    temp = os.path.join(context.Temp.root, "fillfile1")
    context.fillfile(temp)
    assert os.path.exists(temp)  # nosec
    context.rmpath(temp)


def test_x_teardown():
    """Test teardown function last."""
    temp = context.Temp
    path = temp.root
    context.teardown()
    assert not os.path.exists(path)  # nosec
