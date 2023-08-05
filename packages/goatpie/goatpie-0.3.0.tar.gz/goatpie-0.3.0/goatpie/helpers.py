import urllib
from typing import Optional

import pandas
import plotext
from rich import box
from rich.table import Column, Table


def get_domain(url: str, keep_subdomain: bool = False) -> str:
    """
    Extract domain ('example.com'), quick&dirty

    :param url: str Target URL
    :param keep_subdomain: bool Whether to strip subdomain

    :return: str
    """

    # Parse URL
    parsed = urllib.parse.urlparse(url)

    # If input is malformed (eg no scheme, like 'example.com') ..
    if parsed.path == url:
        # .. prepend scheme & try again
        parsed = urllib.parse.urlparse(f"http://{url}")

    # Determine domain
    # (1) Extract network location
    # (2) Remove backslashes (eg '\\192.168.X.Y')
    netloc = parsed.netloc.lstrip("\\")

    # If not keeping subdomain ..
    if not keep_subdomain:
        # .. combine its last two parts (= domain name & tld)
        return ".".join(netloc.split(".")[-2:])

    # .. otherwise keep whole record
    return netloc


def render_stats(
    obj,
    width: int,
    height: int,
    labels: Optional[list] = None,
    colors: Optional[list] = None,
    limit: int = 14,
    step: int = 100,
) -> str:
    """
    Renders visits & pageviews using 'plotext'

    :param obj: goatpie.GoatPie
    :param width: int Plot width
    :param height: int Plot height
    :param labels: list Data labels
    :param colors: list Bar colors
    :param limit: int Limits data to last XY days
    :param step: int Steps used on Y-axis

    :return: str Plotted canvas
    """

    # If not specified ..
    # (1) .. assign default labels
    if labels is None:
        labels = ["Visits", "Pageviews"]

    # (2) .. assign default colors
    if colors is None:
        colors = ["blue", "magenta"]

    # Clear everything
    plotext.clf()
    plotext.clc()

    # Retrieve data
    visits = obj.get_visits(limit)
    pageviews = obj.get_pageviews(limit)

    # Determine relative bar width
    # FIX: Actually calculate something
    bar_width = 0.4

    # Configure plot
    plotext.multiple_bar(
        visits.Day, [visits.Visits, pageviews.Pageviews], label=labels, width=bar_width, marker="hd", color=colors
    )
    plotext.plotsize(width, height)
    plotext.xlabel("hits / day")
    plotext.frame(False)
    plotext.ticks_color("white")
    plotext.ticks_style("bold")
    plotext.xticks([])
    plotext.yticks(range(0, pageviews.Pageviews.max(), step))

    return plotext.build()


def data2table(data: pandas.DataFrame, title: Optional[str] = None, colors: Optional[list] = None) -> Table:
    """
    Creates 'rich' table from 'pandas' dataframe

    :param data: pandas.DataFrame Table data
    :param title: str Table heading
    :param colors: list Column text colors

    :return: rich.table.Table
    """

    # If not specified ..
    if colors is None:
        # .. assign defaults
        colors = ["blue", "white", "cyan"]

    # Create header row
    header = [Column(header=header, justify="right", style=colors[idx]) for idx, header in enumerate(data.columns)]

    # Construct table
    table = Table(
        title=title,
        title_style="bold white",
        header_style="bold white",
        show_lines=False,
        box=box.ROUNDED,
        expand=True,
        *header,
    )

    # Add rows to it
    for row in data.values:
        table.add_row(*[str(cell) for cell in row])

    return table
