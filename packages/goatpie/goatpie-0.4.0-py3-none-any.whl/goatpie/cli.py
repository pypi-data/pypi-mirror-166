import configparser
import os

import click

from .app import GoatPieApp
from .goatpie import GoatPie
from .helpers import get_domain


@click.command()
@click.argument("url")
@click.option("-u", "--update", is_flag=True, help="Forces update of local database")
@click.option("-l", "--limit", default=14, help="Shows visits & pageviews for the last XY days. Default: 14")
@click.option("-b", "--bar-colors", type=str, help="Defines two bar colors. Default: 'blue,magenta'")
@click.option("-t", "--text-colors", type=str, help="Defines three text colors. Default: 'blue,white,cyan'")
@click.version_option("0.4.0")
def cli(url: str, update: bool, limit: int, bar_colors: str, text_colors: str) -> None:
    """
    Provides 'Goatcounter' statistics for URL
    """

    # Determine base directory
    base_dir = click.get_app_dir("goatpie")

    # Configure application
    # (1) Set minimum update interval (in seconds)
    interval = 1 * 60 * 60  # 1 hour

    # (2) Set steps used on Y-axis
    step = 100

    # (3) Set bar colors
    bar_colors_default = "blue,magenta"

    # (4) Set text colors
    text_colors_default = "blue,white,cyan"

    # Initialize config object (using defaults)
    config = configparser.ConfigParser(
        defaults={
            "interval": interval,
            "step": step,
            "bar_colors": bar_colors_default,
            "text_colors": text_colors_default,
        }
    )

    # Get path to config file
    config_file = os.path.join(base_dir, "config.ini")

    # If not existent ..
    if not os.path.exists(config_file):
        # .. create it (using default values)
        with open(config_file, "w", encoding="utf-8") as file:
            config.write(file)

    # Load its contents
    config.read(config_file)

    # Get domain identifier
    domain = get_domain(url, True)

    # If no section for domain ..
    if domain not in config:
        # .. create it & add interval option
        config.add_section(domain)
        config.set(domain, "interval", str(interval))
        config.set(domain, "step", str(step))
        config.set(domain, "bar_colors", bar_colors_default)
        config.set(domain, "text_colors", text_colors_default)

    # If no API token for domain section ..
    if not config.has_option(domain, "token"):
        # .. retrieve it
        token = click.prompt("Please enter your token", hide_input=True, confirmation_prompt=True)

        # If approved ..
        if click.confirm("Save token for later?", default=True):
            # (1) .. save API token
            config.set(domain, "token", token)

            # (2) .. update config file
            with open(config_file, "w", encoding="utf-8") as file:
                config.write(file)

    # Get ready
    obj = GoatPie(url, config[domain].get("token"), base_dir)
    obj.interval = int(config[domain].get("interval", interval))

    # If specified ..
    if update:
        # .. force database update
        obj.update(0)

    # Create application
    app = GoatPieApp

    # Configure it
    app.obj = obj
    app.limit = limit
    app.step = int(config[domain].get("step", step))

    app.bar_colors = (
        config[domain].get("bar_colors", bar_colors_default).split(",")
        if bar_colors is None
        else bar_colors.split(",")
    )

    app.text_colors = (
        config[domain].get("text_colors", text_colors_default).split(",")
        if text_colors is None
        else text_colors.split(",")
    )

    # Run!
    app.run(title='"Goatcounter" analytics', log=os.path.join(base_dir, "app.log"))
