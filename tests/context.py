import os
import shutil
import string
import atexit
import torrentfile
import pyben

TESTS = os.path.dirname(os.path.abspath(__file__))
TESTDIR = os.path.join(TESTS, "TESTDIR")
ROOT = os.path.join(TESTDIR, "Root")


def rmpath(path):
    if os.path.exists(path):
        if os.path.isfile(path):
            os.remove(path)
        elif os.path.isdir(path):
            shutil.rmtree(path)


def testdir(func):
    def wrapper(*args, **kwargs):
        if not os.path.exists(TESTDIR):
            os.mkdir(TESTDIR)
        return func(*args, **kwargs)
    return wrapper


@testdir
def testdata():
    root = ROOT
    dir1 = os.path.join(root, "dir1")
    file1 = os.path.join(root, "file1")
    file2 = os.path.join(root, "file2")
    file3 = os.path.join(dir1, "file3")
    file4 = os.path.join(dir1, "file4")
    for folder in [root, dir1]:
        rmpath(folder)
        os.mkdir(folder)
    text = (string.printable + string.whitespace + string.hexdigits) * 8
    bstring = text.encode("utf-8")
    seqLen = len(bstring)
    for item, size in [(file1,18), (file2,22), (file3,26), (file4,28)]:
        size = 2**size
        with open(item, "wb") as fd:
            while size > 0:
                fd.write(bstring)
                size -= seqLen
    return root


def testtorrent():
    if not os.path.exists(ROOT):
        testdata()
    kws = {
        "announce": "announce.com",
        "announce_list": ["tracker.com", "othertracker.com"],
        "private": True,
        "comment": "Testing TorrentfileGUI",
        "piece_length": 2**17,
        "path": ROOT,
        "source": "Testing",
        "outfile": ROOT + ".torrent"
    }
    torrentv1 = torrentfile.TorrentFile(**kws)
    torrentv1.write()
    return ROOT + ".torrent"


def testmeta():
    torrent = ROOT + ".torrent"
    if not os.path.exists(torrent):
        torrent = testtorrent()
    meta = pyben.load(torrent)
    return meta

@atexit.register
def teardown():
    rmpath(TESTDIR)
