##############################################################################
# Copyright 20** AlexPDev
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
"""Application version id tag."""

import os


__version__ = "0.3.4"


def _conf():
    """Create some enviornment variables."""
    parent = os.path.dirname(__file__)
    assets = os.path.join(parent, "assets")
    path = os.path.relpath(assets, ".")
    return path


ASSETS = str(_conf())
os.environ["ASSETS"] = ASSETS
