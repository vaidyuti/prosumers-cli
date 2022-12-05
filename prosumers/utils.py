import click


def echo_dict(source: dict, spacing=16):
    for key, value in source.items():
        click.echo(
            click.style(f"{key: <{spacing}}:  ", fg="black")
            + click.style(value, bold=True)
        )
