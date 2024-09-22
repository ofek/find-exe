# SPDX-FileCopyrightText: 2024-present Ofek Lev <oss@ofek.dev>
#
# SPDX-License-Identifier: MIT
from __future__ import annotations

import os
import re
import sys
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Callable


def with_prefix(prefix: str, *, mode: int = os.F_OK | os.X_OK, path: str | None = None) -> list[str]:
    """
    Parameters:
        prefix: The prefix used for searching.
        mode: The file mode used for checking access.
        path: The PATH to check. If `None`, the PATH environment variable is used.

    Returns:
        A list of absolute paths to executables that match the given prefix.
    """
    return with_condition(lambda entry: entry.name.startswith(prefix), mode=mode, path=path)


def with_pattern(
    pattern: str | re.Pattern[str], *, mode: int = os.F_OK | os.X_OK, path: str | None = None
) -> list[str]:
    """
    Parameters:
        pattern: The pattern used for searching.
        mode: The file mode used for checking access.
        path: The PATH to check. If `None`, the PATH environment variable is used.

    Returns:
        A list of absolute paths to executables that match the given pattern.
    """
    return with_condition(lambda entry: re.search(pattern, entry.name) is not None, mode=mode, path=path)


def with_condition(
    condition: Callable[[os.DirEntry], bool], *, mode: int = os.F_OK | os.X_OK, path: str | None = None
) -> list[str]:
    """
    Parameters:
        condition: The condition used for searching.
        mode: The file mode used for checking access.
        path: The PATH to check. If `None`, the PATH environment variable is used.

    Returns:
        A list of absolute paths to executables that match the given pattern.
    """
    if path is None:
        path = os.environ.get('PATH', None)
        if path is None:
            path = path_fallback()

    executables: list[str] = []
    if not path:
        return executables

    search_paths = path.split(os.pathsep)
    seen = set()
    for search_path in search_paths:
        if not os.path.isdir(search_path):
            continue

        norm_path = os.path.normcase(search_path)
        if norm_path in seen:
            continue

        seen.add(norm_path)
        with os.scandir(search_path) as entries:
            for entry in entries:
                try:
                    # This may fail but we don't want to do an access check until the end because that is slower
                    if not entry.is_file():
                        continue
                except PermissionError:
                    continue

                if valid_executable(entry.name) and condition(entry) and os.access(entry.path, mode):
                    executables.append(entry.path)

    return executables


if sys.platform == 'win32':
    EXECUTABLE_EXTENSIONS: tuple[str, ...] | None = None

    def _get_executable_extensions() -> tuple[str, ...]:
        global EXECUTABLE_EXTENSIONS  # noqa: PLW0603
        if EXECUTABLE_EXTENSIONS is None:
            pathext = os.environ.get('PATHEXT') or '.COM;.EXE;.BAT;.CMD;.VBS;.JS;.WS;.MSC'
            EXECUTABLE_EXTENSIONS = tuple(ext for ext in pathext.split(os.pathsep) if ext)

        return EXECUTABLE_EXTENSIONS

    def valid_executable(file_name: str) -> bool:
        return file_name.upper().endswith(_get_executable_extensions())

    def path_fallback() -> str:
        return os.defpath

else:

    def valid_executable(file_name: str) -> bool:  # noqa: ARG001
        return True

    def path_fallback() -> str:
        try:
            path = os.confstr('CS_PATH')
        except ValueError:
            path = os.defpath

        return path or ''
