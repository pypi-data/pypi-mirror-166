"""This module contains the main CLI command group."""
from __future__ import annotations

import click

from project_foundry import __version__

__all__ = [
    "cli",
]


@click.group()
@click.version_option(
    __version__,
    "--version",
    "-V",
    prog_name="project-foundry",
)
def cli() -> None:
    """A tool for casting projects from molds."""
    pass  # pragma: no cover
