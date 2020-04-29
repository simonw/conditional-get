from conditional_get import cli
from click.testing import CliRunner
import json


def test_help():
    result = CliRunner().invoke(cli.cli, ["--help"])
    assert 0 == result.exit_code
    assert "Fetch data using HTTP conditional get" in result.output.strip()


def test_performs_conditional_get(mocker):
    m = mocker.patch.object(cli, "httpx")
    m.get.return_value = mocker.Mock()
    m.get.return_value.status_code = 200
    m.get.return_value.content = b"Hello PNG"
    m.get.return_value.headers = {"etag": "hello-etag"}
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(
            cli.cli, ["https://example.com/file.png", "-o", "file.png"]
        )
        m.get.assert_called_once_with("https://example.com/file.png", headers={})
        assert b"Hello PNG" == open("file.png", "rb").read()
        # Should have also written the ETags file
        assert {"https://example.com/file.png": "hello-etag"} == json.load(
            open("etags.json")
        )
        # Second call should eract differently
        m.get.reset_mock()
        m.get.return_value.status_code = 304
        result = runner.invoke(
            cli.cli, ["https://example.com/file.png", "-o", "file.png"]
        )
        m.get.assert_called_once_with(
            "https://example.com/file.png", headers={"If-None-Match": "hello-etag"}
        )
