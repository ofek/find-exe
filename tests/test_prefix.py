# SPDX-FileCopyrightText: 2024-present Ofek Lev <oss@ofek.dev>
#
# SPDX-License-Identifier: MIT
from __future__ import annotations

import os
import sys

import find_exe


def test(monkeypatch) -> None:
    exe_dir = os.path.dirname(sys.executable)
    exe_name = os.path.basename(sys.executable)
    monkeypatch.setenv('PATH', f'{exe_dir}{os.pathsep}{exe_dir}')
    assert sys.executable in find_exe.with_prefix(exe_name)
