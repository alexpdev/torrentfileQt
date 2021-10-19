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


def testDir(func):
    def wrapper(*args, **kwargs):
        if not os.path.exists(TESTDIR):
            os.mkdir(TESTDIR)
        return func(*args, **kwargs)
    return wrapper


def fill(path, exp=25):
    text = (string.printable + string.whitespace + string.hexdigits) * 8
    btext = text.encode("utf-8")
    btextlen = len(btext)
    size = 2 ** exp
    with open(path, "wb") as fd:
        while size >= 0:
            fd.write(btext)
            size -= btextlen
    return path


@testDir
def testfile(val=20):
    root = os.path.join(TESTDIR, "file1")
    fill(root, exp=val)
    return root


@testDir
def testdir():
    root = ROOT
    dir1 = os.path.join(root, "dir1")
    file1 = os.path.join(root, "file1")
    file2 = os.path.join(root, "file2")
    file3 = os.path.join(dir1, "file3")
    file4 = os.path.join(dir1, "file4")
    for folder in [root, dir1]:
        rmpath(folder)
        os.mkdir(folder)
    for file in [file1, file2, file3, file4]:
        fill(file, 26)
    return root


@atexit.register
def teardown():
    rmpath(TESTDIR)
