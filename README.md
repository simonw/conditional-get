# conditional-get

[![PyPI](https://img.shields.io/pypi/v/conditional-get.svg)](https://pypi.python.org/pypi/conditional-get)
[![CircleCI](https://circleci.com/gh/simonw/conditional-get.svg?style=svg)](https://circleci.com/gh/simonw/conditional-get)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/conditional-get/blob/master/LICENSE)

CLI tool for fetching data using HTTP conditional get.

## Installation

    pip install conditional-get

## Usage

    conditional-get https://static.simonwillison.net/static/2020/Simon_Willison__TIL.png

This will save to a filename derived from the URL.

    conditional-get https://static.simonwillison.net/static/2020/Simon_Willison__TIL.png -o til.png

Use `-o` to specify a filename.

By default the ETags for the retrieved URLs will be stored in a `etags.json` file in the current directory.

Use `--etags otherfile.json` to store that file somewhere else.
