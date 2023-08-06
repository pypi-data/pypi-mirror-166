from __future__ import annotations

import pytest
from click.testing import CliRunner

import project_foundry
from project_foundry.cli.main import cli


@pytest.fixture
def runner() -> CliRunner:
    """Construct and return a new CliRunner."""
    return CliRunner()


@pytest.mark.parametrize("option", ["--version", "-V"])
def test_version_option(runner: CliRunner, option: str) -> None:
    result = runner.invoke(cli, [option])
    assert result.exit_code == 0
    assert result.output == f"project-foundry, version {project_foundry.__version__}\n"
