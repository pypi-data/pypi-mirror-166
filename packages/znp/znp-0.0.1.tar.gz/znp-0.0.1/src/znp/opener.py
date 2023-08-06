#!/bin/python3
import sys
import os
import re
import magic
from ewmh import EWMH
import dbus
import subprocess
import time


class NoFileOrDirectory(Exception):
    """
    Exception raised when user did not give a complete path
    to the current zathura file
    """

    def __init__(
        self, dir_path, file_path, message="ERROR: No directory or file found"
    ):
        self.file = file_path
        self.dir = dir_path
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.message}\nFile: "{self.file}"\nDir: "{self.dir}"'


def filter_file(test_file):
    """
    Returns true if file is not a known file type zathura
    """
    mime = magic.Magic(mime=True)
    file_type = mime.from_file(test_file)
    accepted_types = [
        "image/vnd.djvu",
        "application/epub+zip",
        "application/postscript",
        "application/zip",
        "application/pdf",
    ]
    if file_type in accepted_types:
        return False

    return True


def get_next_or_prev_file(current_file_path, next_file=False, prev_file=False):
    """
    Get the next file in a directory when given a file path
    """
    # Split the path into directory and file
    temp = os.path.split(current_file_path)
    directory = temp[0]
    current_file = temp[1]
    # Check that both directory and file are not empty
    if not directory or not current_file:
        # If they are empty raise an error and exit with status 1
        raise NoFileOrDirectory(dir_path=directory, file_path=current_file)

    # Get a (sorted) list of files from the given directory
    file_list = os.listdir(directory)
    file_list.sort()

    # Populate vars
    new_index = 0
    incrementor = 0
    range_limit = 0
    reset_val = 0

    # Set vars depending on next or prev
    if next_file:
        incrementor = 1
        range_limit = len(file_list)
        reset_val = 0
    elif prev_file:
        incrementor = -1
        range_limit = -1
        reset_val = len(file_list) - 1

    # Add one to the given files index to get the next file
    if current_file in file_list:
        new_index = file_list.index(current_file) + incrementor

    # Check if we are out of bounds
    if next_file and new_index >= len(file_list):
        new_index = reset_val
    elif prev_file and new_index < 0:
        new_index = reset_val

    next_or_prev_file = os.path.join(directory, file_list[new_index])

    # Test if next_or_prev_file is valid file
    for i in range(new_index, range_limit, incrementor):
        next_or_prev_file = os.path.join(directory, file_list[i])
        if os.path.isfile(next_or_prev_file) and not filter_file(next_or_prev_file):
            return next_or_prev_file

    # File was not found so we start from the beginning / end
    new_index = reset_val
    for i in range(new_index, range_limit, incrementor):
        next_or_prev_file = os.path.join(directory, file_list[i])
        if os.path.isfile(next_or_prev_file) and not filter_file(next_or_prev_file):
            return next_or_prev_file

    """Old method"""
    # if current_file in file_list:
    #     if next_file:
    #         new_index = file_list.index(current_file) + 1
    #     elif prev_file:
    #         new_index = file_list.index(current_file) - 1

    # if next_file:
    #     # Check if we are out of bounds
    #     if new_index >= len(file_list):
    #         new_index = 0

    #     next_or_prev_file = os.path.join(directory, file_list[new_index])

    #     # Test if next_or_prev_file is valid file
    #     for i in range(new_index, len(file_list)):
    #         next_or_prev_file = os.path.join(directory, file_list[i])
    #         if os.path.isfile(next_or_prev_file) and not filter_file(next_or_prev_file):
    #             return next_or_prev_file

    #     # File was not found so we start from the beginning
    #     new_index = 0
    #     for i in range(new_index, len(file_list)):
    #         next_or_prev_file = os.path.join(directory, file_list[i])
    #         if os.path.isfile(next_or_prev_file) and not filter_file(next_or_prev_file):
    #             return next_or_prev_file

    # elif prev_file:
    #     # Check if we are out of bounds
    #     if new_index < 0:
    #         new_index = len(file_list) - 1

    #     next_or_prev_file = os.path.join(directory, file_list[new_index])

    #     # Test if next_or_prev_file is valid file
    #     for i in range(new_index, -1, -1):
    #         next_or_prev_file = os.path.join(directory, file_list[i])
    #         if os.path.isfile(next_or_prev_file) and not filter_file(next_or_prev_file):
    #             return next_or_prev_file

    #     # File was not found so we start from the end
    #     new_index = len(file_list) - 1
    #     for i in range(new_index, -1, -1):
    #         next_or_prev_file = os.path.join(directory, file_list[i])
    #         if os.path.isfile(next_or_prev_file) and not filter_file(next_or_prev_file):
    #             return next_or_prev_file

    # If the current file is the only compatible file then return None
    return None


def get_pid():
    """
    Use ewmh to get the pid of the focused window.
    This should be zathura assuming it znp was run from
    zathura and user is using X11
    """
    ewmh = EWMH()
    win = ewmh.getActiveWindow()
    zpid = ewmh.getWmPid(win)

    return zpid


def zathura_open(file_path, zpid=None, next_file=False, prev_file=False):
    """
    Open file in zathura optionally open the next file in
    the directory of the given file
    """

    if not zpid:
        zpid = get_pid()

    if not zpid:
        return 1

    if next_file or prev_file:
        try:
            file_path = get_next_or_prev_file(
                file_path, next_file=next_file, prev_file=prev_file
            )
        except NoFileOrDirectory as err:
            print(err, file=sys.stderr)
            return 1

        # If current file is the only eligible file exit gracefully
        if not file_path:
            return 0

    # Test that given file is actually a file if not finding next_or_prev
    elif not os.path.isfile(file_path):
        print(f"Given file is not a file: {file_path}", file=sys.stderr)
        return 1

    # zathuraPopen = subprocess.Popen(["zathura", "--log-level=debug"])
    zathuraName = "org.pwmt.zathura.PID-" + str(zpid)
    # time.sleep(0.5)

    zathuraObject = dbus.SessionBus().get_object(zathuraName, "/org/pwmt/zathura")
    zathuraDBus = dbus.Interface(zathuraObject, "org.pwmt.zathura")

    zathuraDBus.OpenDocument(
        file_path,
        "",
        0,
    )

    return 0
