import click

from .config import inspect_config, list_config_envs


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
    click.echo("Verifying '{0}'".format(scenario))


@click.command()
@click.argument("scenario", default="scenario.yaml", required=False)
def verify(scenario):
    """Verifies the integrity of the scenario file."""
    click.echo("Verifying '{0}'".format(scenario))


@click.command()
@click.argument("env", default="local", required=False)
def config(env):
    """Show/edit the configurations of various environments."""
    env_config = inspect_config(env)
    if env_config:
        env_config.detail()
    else:
        click.echo(
            click.style(
                "No configuration for '{0}' env was found.".format(env), fg="yellow"
            )
        )


@click.command()
def list_configs():
    """Lists all configured environments."""
    envs = list_config_envs()
    if envs:
        click.echo(click.style("{0} environments found.".format(len(envs)), fg="black"))
        for env in envs:
            click.echo(env)
    else:
        click.echo(click.style("No environments configured.", fg="black"))


cli.add_command(run)
cli.add_command(verify)
cli.add_command(config)
cli.add_command(list_configs, "list")
