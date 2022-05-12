# TorrentFileQt

![torrentfileQt.png](./assets/torrentfileQt.png)

---------
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/065ca999772a434ba1aadae05f8b6bc7)](https://www.codacy.com/gh/alexpdev/torrentfileQt/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=alexpdev/torrentfileQt&amp;utm_campaign=Badge_Grade)
[![codecov](https://codecov.io/gh/alexpdev/torrentfileQt/branch/main/graph/badge.svg?token=S5Q9CRD6C2)](https://codecov.io/gh/alexpdev/torrentfileQt)
![PyPI - License](https://img.shields.io/pypi/l/torrentfileQt?color=orange&style=plastic)
![PyPI - Downloads](https://img.shields.io/pypi/dw/torrentfileQt?style=plastic)
![CI Workflow](https://img.shields.io/github/workflow/status/alexpdev/torrentfileQt/CI)
![last commit](https://img.shields.io/github/last-commit/alexpdev/torrentfileQt?color=blue)
[![Codacy Badge](https://app.codacy.com/project/badge/Coverage/065ca999772a434ba1aadae05f8b6bc7)](https://www.codacy.com/gh/alexpdev/torrentfileQt/dashboard?utm_source=github.com&utm_medium=referral&utm_content=alexpdev/torrentfileQt&utm_campaign=Badge_Coverage)

TorrentFileQt is a GUI Frontend for [TorrentFile CLI](https://github.com/alexpdev/torrentfile) project.

## Features

- Create .torrent files
- Display detailed information for a .torrent file
- Bittorrent v1, v2 and hybrid .torrent files supported
- Check if a .torrent file contents are in filesystem
- Check progress or percentage complete for .torrent file
- Edit torrent files.

## Requirements

- Pyside6
- torrentfile

## ScreenShots

![createtorrent.png](./assets/screenshots/create-tab.png)

---------

![checktorrent.png](./assets/screenshots/recheck-tab.png)

---------

![edittorrent.png](./assets/screenshots/edit-tab.png)

---------

![torrentinfo.png](./assets/screenshots/info-tab.png)

---------

## Install

- From git:

```bash
git clone https://github.com/alexpdev/torrentfileQt.git
cd torrentfileQt
pip install -r requirements.txt
pip install .
torrentfileQt
```

- From PyPi

```bash
pip install torrentfileQt
torrentfileQt
```

> Alternatively you can download a precompiled binary from the release page.
