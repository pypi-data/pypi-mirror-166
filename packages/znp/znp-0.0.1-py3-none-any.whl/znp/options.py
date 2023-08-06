#!/usr/bin/env python3
import argparse


def get_opts(prog_name="znp"):
    parser = argparse.ArgumentParser(
        prog=prog_name,
        description="""Add a file to a given instance of zathura""",
        allow_abbrev=False,
    )
    parser.add_argument(
        "-n",
        "--next",
        action="store_true",
        help="Go to the next file in the directory of the given file",
    )
    parser.add_argument(
        "-p",
        "--prev",
        action="store_true",
        help="Go to the prev file in the directory of the given file",
    )
    parser.add_argument(
        "-P",
        "--pid",
        metavar="PID",
        default=None,
        help="""PID of the zathura instance to use.
        Default is the active window detected via ewmh""",
    )
    parser.add_argument("file", metavar="FILE", type=str, help="The file to open")
    args = parser.parse_args()
    return args
