# conditional-get

[![PyPI](https://img.shields.io/pypi/v/conditional-get.svg)](https://pypi.python.org/pypi/conditional-get)
[![CircleCI](https://circleci.com/gh/simonw/conditional-get.svg?style=svg)](https://circleci.com/gh/simonw/conditional-get)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/conditional-get/blob/master/LICENSE)

CLI tool for fetching data using [HTTP conditional get](https://developer.mozilla.org/en-US/docs/Web/HTTP/Conditional_requests).

## Installation

    pip install conditional-get

## Usage

The first time you run this command it will download the file and store the ETag (if one was returned) in a file called `etags.json`.

The second time you run this command against the same URL it will use that ETag, potentially resulting in a `304 Not Modified` response which saves bandwidth by not re-downloading the file.

    # First run - will fetch the file
    conditional-get https://static.simonwillison.net/static/2020/Simon_Willison__TIL.png
    # Second run - will only fetch the file if it has changed
    conditional-get https://static.simonwillison.net/static/2020/Simon_Willison__TIL.png

The filename will be derived from the URL. You can customize the filename using the `-o` option:

    conditional-get https://static.simonwillison.net/static/2020/Simon_Willison__TIL.png -o til.png

By default the ETags for the retrieved URLs will be stored in a `etags.json` file in the current directory. You can use the `--etags otherfile.json` to store that file somewhere else:

    conditional-get https://static.simonwillison.net/static/2020/Simon_Willison__TIL.png --etags my-etags.json

Use the `-v` option to get debug output showing what is happening:

    $ conditional-get https://static.simonwillison.net/static/2020/Simon_Willison__TIL.png -v
    Response status code: 200
    [####################################]  100%

    $ ls
    Simon_Willison__TIL.png	etags.json

    $ cat etags.json 
    {
        "https://static.simonwillison.net/static/2020/Simon_Willison__TIL.png": "\"d65b78782dfa93213c99099e0e2181d8\""
    }

    $ conditional-get https://static.simonwillison.net/static/2020/Simon_Willison__TIL.png -v
    Existing ETag: "d65b78782dfa93213c99099e0e2181d8"
    Response status code: 304
