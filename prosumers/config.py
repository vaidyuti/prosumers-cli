import yaml
from dataclasses import dataclass
import click


@dataclass
class Environment:
    """Defines the structure of an environment"""

    mqtt_server: str
    dex_server: str


def load_config() -> dict[str, Environment] | None:
    try:
        with open("config.yaml", "r") as stream:
            data = yaml.safe_load(stream)
            return data
    except yaml.YAMLError as ex:
        click.echo(click.style(ex, fg="red"))
    except Exception as ex:
        click.echo(click.style(ex, fg="red"))


def inspect_config(env: str) -> Environment | None:
    config = load_config()
    if config:
        return config.get(env)


def list_config_envs():
    config = load_config()
    if config:
        return list(config.keys())
