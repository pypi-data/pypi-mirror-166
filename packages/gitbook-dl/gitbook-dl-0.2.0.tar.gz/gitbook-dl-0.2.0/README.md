# gitbook-dl

Command-line program to download books from gitbook.com

:warning: _This package is currently under development_

## Purpose

## Get Started

### Installing

The easiest way to install `gitbook-dl` is via `pip`:

```console
pip install gitbook-dl
```

## Contributing

### Developer Guide

1. Clone this repository `git clone git@github.com:alwinw/gitbook-dl.git`
2. Install the development version `pip install -v -e .[<extras>]` (`-e` needs pip >= 22.0 for pyproject.toml) or `poetry install --extras "<extras>"`
3. Make your changes and commit using [commitizen](https://commitizen-tools.github.io/commitizen/#installation) and ensure [pre-commit](https://pre-commit.com/#install) is active
4. When bumping version, use `cz bump -ch -cc`
5. When ready, bump the version and run `poetry build -v`. If deploying, run `poetry publish --build -v`
