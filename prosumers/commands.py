from click import echo, style
import click

from .config import inspect_config, list_config_envs, load_config
from .scenario import read_scenario
from .core import RunnableScenario


def config(env, all):
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


def list_configs():
    envs = list_config_envs()
    if envs:
        echo(style("{0} environments found.".format(len(envs)), fg="black"))
        for env in envs:
            echo(env)
    else:
        echo(style("No environments configured.", fg="black"))


def verify(scenario):
    echo("Verifying '{0}'...".format(scenario))
    try:
        obj = read_scenario(scenario)
        echo(click.style(f"Verified.", fg="bright_green", bold=True))
    except Exception as ex:
        echo(click.style(ex, fg="red"))


def run(scenario, env, verbose):
    try:
        env_obj = inspect_config(env)
        scenario_obj = read_scenario(scenario)
        process = RunnableScenario(scenario_obj, env_obj)
        process.run()
    except Exception as ex:
        echo(click.style(ex, fg="red"))
