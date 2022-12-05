import click
from click import echo, style

from .config import inspect_config, list_config_envs, load_config
from .scenario import read_scenario


@click.group()
def cli():
    """A CLI tool to emulate prosumers for testing the DEX platform."""
    pass


@click.command()
@click.argument("scenario", default="scenario.yaml", required=False)
@click.option("--env", "-e", default="local", help="Run in verbose mode.")
@click.option("--verbose", "-v", is_flag=True, help="Run in verbose mode.")
def run(scenario, env, verbose):
    """Runs the emulation with the scenario file."""
    echo("Verifying '{0}'".format(scenario))


@click.command()
@click.argument("scenario", default="scenario.yaml", required=False)
def verify(scenario):
    """Verifies the integrity of the scenario file."""
    echo("Verifying '{0}'...".format(scenario))
    try:
        obj = read_scenario(scenario)
        echo(click.style(f"Verified.", fg="bright_green", bold=True))
    except Exception as ex:
        echo(click.style(ex, fg="red", bold=True))


@click.command()
@click.argument("env", default="local", required=False)
@click.option("--all", "-a", is_flag=True, help="Show all configurations.")
def config(env, all):
    """Show/edit the configurations of various environments."""
    if all:
        config = load_config()
        if config != None:
            envs = config.values()
            echo(style("{0} environments found.\n".format(len(envs)), fg="black"))
            div = style("-" * 64, fg="black")
            echo(div)
            for env in envs:
                env.detail()
                echo(div)
    else:
        env_config = inspect_config(env)
        if env_config:
            env_config.detail()
        else:
            echo(style("No config for '{0}' env was found.".format(env), fg="yellow"))


@click.command()
def list_configs():
    """Lists all configured environments."""
    envs = list_config_envs()
    if envs:
        echo(style("{0} environments found.".format(len(envs)), fg="black"))
        for env in envs:
            echo(env)
    else:
        echo(style("No environments configured.", fg="black"))


cli.add_command(run)
cli.add_command(verify)
cli.add_command(config)
cli.add_command(list_configs, "list")
