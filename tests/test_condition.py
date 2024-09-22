# SPDX-FileCopyrightText: 2024-present Ofek Lev <oss@ofek.dev>
#
# SPDX-License-Identifier: MIT
from __future__ import annotations

import os
import sys
from unittest.mock import patch

import pytest

import find_exe


def test_empty_path() -> None:
    assert find_exe.with_condition(bool, path='') == []


@pytest.mark.skipif(sys.platform != 'win32', reason='Requires Windows')
def test_path_fallback(monkeypatch) -> None:
    monkeypatch.delenv('PATH', raising=False)
    with patch('os.defpath', ''):
        assert find_exe.with_condition(bool) == []


@pytest.mark.skipif(sys.platform == 'win32', reason='Requires Unix')
def test_path_fallback_unix(monkeypatch) -> None:
    monkeypatch.delenv('PATH', raising=False)
    with patch('os.confstr', side_effect=ValueError), patch('os.defpath', ''):
        assert find_exe.with_condition(bool) == []


def test_no_match() -> None:
    assert find_exe.with_condition(lambda _: False) == []


def test_handle_file_in_path(monkeypatch) -> None:
    monkeypatch.setenv('PATH', __file__, os.pathsep)
    assert find_exe.with_condition(lambda _: False) == []


def test_duplicate_path(monkeypatch) -> None:
    exe_dir = os.path.dirname(sys.executable)
    exe_name = os.path.basename(sys.executable)
    monkeypatch.setenv('PATH', f'{exe_dir}{os.pathsep}{exe_dir}')
    assert find_exe.with_condition(lambda entry: entry.name == exe_name) == [sys.executable]
