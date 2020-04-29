from conditional_get import cli
from click.testing import CliRunner


def test_help():
    result = CliRunner().invoke(cli.cli, ["--help"])
    assert 0 == result.exit_code
    assert "Fetch data using HTTP conditional get" in result.output.strip()
