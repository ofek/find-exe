# find-exe

| | |
| --- | --- |
| CI/CD | [![CI - Test](https://github.com/ofek/find-exe/actions/workflows/test.yml/badge.svg)](https://github.com/ofek/find-exe/actions/workflows/test.yml) [![CD - Build](https://github.com/ofek/find-exe/actions/workflows/build.yml/badge.svg)](https://github.com/ofek/find-exe/actions/workflows/build.yml) [![Coverage](https://img.shields.io/codecov/c/gh/ofek/find-exe?token=0CYRLWA98C)](https://app.codecov.io/gh/ofek/find-exe) |
| Docs | [![Docs](https://github.com/ofek/find-exe/actions/workflows/docs.yml/badge.svg)](https://github.com/ofek/find-exe/actions/workflows/docs.yml) |
| Package | [![PyPI - Version](https://img.shields.io/pypi/v/find-exe.svg?logo=pypi&label=PyPI&logoColor=gold)](https://pypi.org/project/find-exe/) [![PyPI - Python Version](https://img.shields.io/pypi/pyversions/find-exe.svg?logo=python&label=Python&logoColor=gold)](https://pypi.org/project/find-exe/) |
| Meta | [![Hatch project](https://img.shields.io/badge/%F0%9F%A5%9A-Hatch-4051b5.svg)](https://github.com/ofek/find-exe) [![linting - Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff) [![types - Mypy](https://img.shields.io/badge/types-Mypy-blue.svg)](https://github.com/python/mypy) [![License - MIT](https://img.shields.io/badge/license-MIT-9400d3.svg)](https://spdx.org/licenses/) [![GitHub Sponsors](https://img.shields.io/github/sponsors/ofek?logo=GitHub%20Sponsors&style=social)](https://github.com/sponsors/ofek) |

-----

This provides a library and CLI (`find-exe`) to find all executables given certain criteria.

```pycon
>>> import find_exe
>>> find_exe.with_prefix("py")
['/usr/bin/python', ...]
```

## Installation

```console
pip install find-exe
```

## Documentation

The [documentation](https://ofek.dev/find-exe/) is made with [Material for MkDocs](https://github.com/squidfunk/mkdocs-material) and is hosted by [GitHub Pages](https://docs.github.com/en/pages).

## License

`find-exe` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.