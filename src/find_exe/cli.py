# SPDX-FileCopyrightText: 2024-present Ofek Lev <oss@ofek.dev>
#
# SPDX-License-Identifier: MIT
from __future__ import annotations

from argparse import ArgumentParser

import find_exe


def main() -> None:
    parser = ArgumentParser(prog='find-exe', description='Find matching executables')
    parser.add_argument('pattern', help='Regular expression to match against the beginning of executable names')
    args = parser.parse_args()

    executables = find_exe.with_pattern(f'^{args.pattern}')
    for executable in executables:
        print(executable)  # noqa: T201
