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


def with_prefix(
    prefix: str,
    *,
    paths: list[str] | None = None,
    path: str | None = None,
    mode: int = os.F_OK | os.X_OK,
) -> list[str]:
    """
    Parameters:
        prefix: The prefix used for searching.
        paths: The list of paths to check. If `None`, the mutually exclusive `path` parameter is used.
        path: The PATH to check, with each path separated by [`os.pathsep`][]. If `None`, the PATH environment
            variable is used. Mutually exclusive with `paths`.
        mode: The file mode used for checking access.

    Returns:
        A list of absolute paths to executables that start with the given prefix.
    """
    return with_condition(lambda entry: entry.name.startswith(prefix), paths=paths, path=path, mode=mode)


def with_pattern(
    pattern: str | re.Pattern[str],
    *,
    paths: list[str] | None = None,
    path: str | None = None,
    mode: int = os.F_OK | os.X_OK,
) -> list[str]:
    """
    Parameters:
        pattern: The pattern used for searching.
        paths: The list of paths to check. If `None`, the mutually exclusive `path` parameter is used.
        path: The PATH to check, with each path separated by [`os.pathsep`][]. If `None`, the PATH environment
            variable is used. Mutually exclusive with `paths`.
        mode: The file mode used for checking access.

    Returns:
        A list of absolute paths to executables that match the given pattern.
    """
    return with_condition(lambda entry: re.search(pattern, entry.name) is not None, paths=paths, path=path, mode=mode)


def with_condition(
    condition: Callable[[os.DirEntry], bool],
    *,
    paths: list[str] | None = None,
    path: str | None = None,
    mode: int = os.F_OK | os.X_OK,
) -> list[str]:
    """
    Parameters:
        condition: The condition used for searching.
        paths: The list of paths to check. If `None`, the mutually exclusive `path` parameter is used.
        path: The PATH to check, with each path separated by [`os.pathsep`][]. If `None`, the PATH environment
            variable is used. Mutually exclusive with `paths`.
        mode: The file mode used for checking access.

    Returns:
        A list of absolute paths to executables that satisfy the given condition.
    """

    search_paths: list[str] = []
    if paths is not None:
        if path is not None:
            message = 'the `paths` and `path` parameters are mutually exclusive'
            raise ValueError(message)

        search_paths[:] = paths
    elif path is not None:
        search_paths[:] = path.split(os.pathsep)
    else:
        path = os.environ.get('PATH', None)
        if path is None:
            path = path_fallback()

        search_paths[:] = path.split(os.pathsep)

    executables: list[str] = []
    seen = set()
    for search_path in search_paths:
        if not (search_path and os.path.isdir(search_path)):
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
            EXECUTABLE_EXTENSIONS = tuple(ext for ext in pathext.casefold().split(os.pathsep) if ext)

        return EXECUTABLE_EXTENSIONS

    def valid_executable(file_name: str) -> bool:
        return file_name.casefold().endswith(_get_executable_extensions())

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
