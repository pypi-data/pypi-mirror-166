#!/usr/bin/env python3
import sys
from .options import get_opts
from .opener import zathura_open


__license__ = "GPL-v3.0"


def main():
    args = get_opts()
    return zathura_open(
        file_path=args.file,
        next_file=args.next,
        prev_file=args.prev,
    )


if __name__ == "__main__":
    sys.exit(main())
