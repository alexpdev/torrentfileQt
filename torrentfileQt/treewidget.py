import os

def sortfiles(path):
    """Sort entries in path.

    Args:
        path (`str`): Target directory for sorting contents.

    Yields:
        item, full (`str`, `str`): Next item in sorted order.
    """
    items = sorted(os.listdir(path), key=str.lower)
    for item in items:
        full = os.path.join(path, item)
        yield item, full

def filelist_total(path):
    """Search directory tree for files.

    Args:
      path (`str`): Path to file or directory base
      sort (`bool`): Return list sorted. Defaults to False.

    Returns:
      (`list`): All file paths within directory tree.
    """
    if os.path.isfile(path):
        file_size = os.path.getsize(path)
        return file_size, [path]
    total = 0
    filelist = []
    if os.path.isdir(path):
        for _, full in sortfiles(path):
            size, paths = filelist_total(full)
            total += size
            filelist.extend(paths)
    return total, filelist


def filelist_total1(path):
    """Search directory tree for files.

    Args:
      path (`str`): Path to file or directory base
      sort (`bool`): Return list sorted. Defaults to False.

    Returns:
      (`list`): All file paths within directory tree.
    """
    if os.path.isfile(path):
        file_size = os.path.getsize(path)
        return file_size, [path]

    # put all files into filelist within directory
    files = []
    total_size = 0
    filelist = sorted(os.listdir(path), key=str.lower)

    for name in filelist:
        full = os.path.join(path, name)
        size, paths = filelist_total(full)
        total_size += size
        files.extend(paths)
    return total_size, files


if __name__ == "__main__":
    path = "./torrentfileQt"
    print(filelist_total(path))
    print(filelist_total1(path))
