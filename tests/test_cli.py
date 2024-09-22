# SPDX-FileCopyrightText: 2024-present Ofek Lev <oss@ofek.dev>
#
# SPDX-License-Identifier: MIT
from __future__ import annotations

import os
import sys
from unittest.mock import patch

from find_exe.cli import main


def test(monkeypatch) -> None:
    exe_dir = os.path.dirname(sys.executable)
    exe_name = os.path.basename(sys.executable)
    monkeypatch.setenv('PATH', f'{exe_dir}{os.pathsep}{exe_dir}')

    executables: list[str] = []
    with patch('sys.argv', ['find_exe', f'{exe_name}$']), patch('find_exe.cli.print', side_effect=executables.append):
        main()

    assert executables == [sys.executable]
