import yaml
from dataclasses import dataclass
from typing import Optional
import click
from .utils import echo_dict


@dataclass
class Env:
    """Defines the structure of an environment"""

    _env: Optional[str]

    mqtt_server: str
    dex_server: str

    def detail(self):
        if self._env:
            echo_dict({"environment": click.style(self._env, fg="bright_green")}),
        rest = self.__dict__
        rest.pop("_env")
        echo_dict(rest)


def load_config() -> dict[str, Env] | None:
    try:
        with open("config.yaml", "r") as stream:
            data = yaml.safe_load(stream)
            return {k: Env(_env=k, **v) for k, v in data.items()} if data else None
    except yaml.YAMLError as ex:
        click.echo(click.style(ex, fg="red"))
    except Exception as ex:
        click.echo(click.style(ex, fg="red"))


def inspect_config(env: str) -> Env | None:
    config = load_config()
    if config:
        return config.get(env)


def list_config_envs():
    config = load_config()
    if config:
        return list(config.keys())
