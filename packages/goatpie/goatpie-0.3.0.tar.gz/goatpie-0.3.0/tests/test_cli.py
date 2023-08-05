from click.testing import CliRunner

from goatpie.cli import cli


def test_cli():
    """
    Tests CLI interface
    """

    # Setup
    # (1) CLI runner
    runner = CliRunner()

    # Run function #1
    result1 = runner.invoke(cli)

    # Assert result
    assert result1.exit_code == 2
