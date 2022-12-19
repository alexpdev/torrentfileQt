# TorrentFileQt

![torrentfileQt.png](./assets/torrentfileQt.png)

* * *

[![Codacy Badge](https://app.codacy.com/project/badge/Grade/065ca999772a434ba1aadae05f8b6bc7)](https://www.codacy.com/gh/alexpdev/torrentfileQt/dashboard?utm_source=github.com&utm_medium=referral&utm_content=alexpdev/torrentfileQt&utm_campaign=Badge_Grade)
[![codecov](https://codecov.io/gh/alexpdev/torrentfileQt/branch/main/graph/badge.svg?token=S5Q9CRD6C2)](https://codecov.io/gh/alexpdev/torrentfileQt)
![PyPI - License](https://img.shields.io/pypi/l/torrentfileQt?color=orange&style=plastic)
![PyPI - Downloads](https://img.shields.io/pypi/dw/torrentfileQt?style=plastic)
![CI Workflow](https://img.shields.io/github/workflow/status/alexpdev/torrentfileQt/CI)
![last commit](https://img.shields.io/github/last-commit/alexpdev/torrentfileQt?color=blue)
[![Codacy Badge](https://app.codacy.com/project/badge/Coverage/065ca999772a434ba1aadae05f8b6bc7)](https://www.codacy.com/gh/alexpdev/torrentfileQt/dashboard?utm_source=github.com&utm_medium=referral&utm_content=alexpdev/torrentfileQt&utm_campaign=Badge_Coverage)

TorrentFileQt is a GUI Frontend for [TorrentFile CLI](https://github.com/alexpdev/torrentfile) project.

## Features

-   Create .torrent files
-   Display detailed information for a .torrent file
-   Bittorrent v1, v2 and hybrid .torrent files supported
-   Check if a .torrent file contents are in filesystem
-   Check progress or percentage complete for .torrent file
-   Edit torrent files
-   Drag and drop files onto any tab
-   Create magnet link URIs
-   Analyze piece lengths for torrent files
-   Now with full Bencode edit support

## Requirements

-   Python 3.6+
-   Pyside6
-   torrentfile

## Usage Overview

![edittorrent.png](https://raw.githubusercontent.com/alexpdev/torrentfileQt/main/assets/TorrentFileQt.gif)

* * *

## Install

-   From git:

```bash
git clone https://github.com/alexpdev/torrentfileQt.git
cd torrentfileQt
pip install -r requirements.txt
pip install .
torrentfileQt
```

-   From PyPi

```bash
pip install torrentfileQt
torrentfileQt
```

> Alternatively you can download a precompiled binary from the release page.

## Issues

To report a bug or ask for a new feature please [open an issue](https://github.com/alexpdev/torrentfileQt/issues) on github.

## License

[Apache 2.0 Software License](./LICENSE)
