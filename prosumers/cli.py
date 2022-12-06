import click
from click import echo, style

from .config import inspect_config, list_config_envs, load_config
from . import commands


@click.group()
def cli():
    """A CLI tool to emulate prosumers for testing the DEX platform."""


@click.command()
def list_configs():
    """Lists all configured environments."""
    commands.list_configs()


@click.command()
@click.argument("env", default="local", required=False)
@click.option("--all", "-a", is_flag=True, help="Show all configurations.")
def config(env, all):
    """Show/edit the configurations of various environments."""
    commands.config()


@click.command()
@click.argument("scenario", default="scenario.yaml", required=False)
def verify(scenario):
    """Verifies the integrity of the scenario file."""
    commands.verify(scenario)


@click.command()
@click.argument("scenario", default="scenario.yaml", required=False)
@click.option("--env", "-e", default="local", help="Run in verbose mode.")
@click.option("--verbose", "-v", is_flag=True, help="Run in verbose mode.")
def run(scenario, env, verbose):
    """Runs the emulation with the scenario file."""
    commands.run(scenario, env, verbose)


cli.add_command(run)
cli.add_command(verify)
cli.add_command(config)
cli.add_command(list_configs, "list")
