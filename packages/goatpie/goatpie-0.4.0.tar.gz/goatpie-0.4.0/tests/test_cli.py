from click.testing import CliRunner

from goatpie.cli import cli


def test_cli():
    """
    Tests CLI interface
    """

    # Setup
    # (1) CLI runner
    runner = CliRunner()

    # Run function
    result = runner.invoke(cli)

    # Assert result
    assert result.exit_code == 2
