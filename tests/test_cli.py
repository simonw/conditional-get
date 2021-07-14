from conditional_get import cli
from click.testing import CliRunner
import pytest
import json


def test_help():
    result = CliRunner().invoke(cli.cli, ["--help"])
    assert 0 == result.exit_code
    assert "Fetch data using HTTP conditional get" in result.output.strip()


@pytest.mark.parametrize("key", (None, "CustomKey"))
def test_performs_conditional_get(mocker, key):
    m = mocker.patch.object(cli, "httpx")
    m.stream.return_value.__enter__.return_value = mocker.Mock()
    m.stream.return_value.__enter__.return_value.status_code = 200
    m.stream.return_value.__enter__.return_value.iter_bytes.return_value = [
        b"Hello PNG"
    ]
    m.stream.return_value.__enter__.return_value.headers = {"etag": "hello-etag"}
    runner = CliRunner()
    with runner.isolated_filesystem():
        args = ["https://example.com/file.png", "-o", "file.png"]
        if key is not None:
            args += ["--key", key]
        result = runner.invoke(cli.cli, args)
        m.stream.assert_called_once_with(
            "GET", "https://example.com/file.png", headers={}
        )
        assert b"Hello PNG" == open("file.png", "rb").read()
        # Should have also written the ETags file
        expected_key = key or "https://example.com/file.png"
        assert {expected_key: "hello-etag"} == json.load(open("etags.json"))
        # Second call should react differently
        m.stream.reset_mock()
        m.stream.return_value.status_code = 304
        result = runner.invoke(cli.cli, args)
        assert result.exit_code == 0
        m.stream.assert_called_once_with(
            "GET",
            "https://example.com/file.png",
            headers={"If-None-Match": "hello-etag"},
        )


@pytest.mark.parametrize(
    "url,content_type,filename",
    [
        ("https://example.com/file.png", "image/png", "file.png"),
        ("https://example.com/", "text/html", "index.html"),
        ("https://example.com/", "text/plain", "index.txt"),
    ],
)
def test_default_filename(mocker, url, content_type, filename):
    m = mocker.patch.object(cli, "httpx")
    m.stream.return_value.__enter__.return_value = mocker.Mock()
    m.stream.return_value.__enter__.return_value.status_code = 200
    m.stream.return_value.__enter__.return_value.iter_bytes.return_value = [b"Hello"]
    m.stream.return_value.__enter__.return_value.headers = {
        "etag": "hello-etag",
        "content-type": content_type,
    }
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(cli.cli, [url])
        assert result.exit_code == 0
        assert b"Hello" == open(filename, "rb").read()
