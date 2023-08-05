import urllib
from typing import Optional

import pandas
import pycountry
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


def get_device(size: str) -> str:
    """
    Converts screen size to device type (if applicable)

    :param size: str Screen size (w,h,dpi)

    :return: str Device type (if matched), otherwise 'unknown'
    """

    # Remove whitespaces
    size = "".join(size.split())

    try:
        # Determine largest value (width OR height)
        size = int(max(map(int, size.split(","))))

    except ValueError:
        # .. report back
        return "Unknown devices"

    # Map screen size to device type
    if size >= 3000:
        return "Computer monitors larger than HD"

    if size >= 1920:
        return "Computer monitors"

    if size >= 1100:
        return "Tablets and small laptops"

    if size >= 1000:
        return "Large phones, small tablets"

    if size >= 300:
        return "Phones"

    return "Unknown devices"


def get_country(code: str) -> str:
    """
    Converts country code to country name (if applicable)

    :param code: str Country code

    :return: str Country name (if successful), otherwise country code
    """

    # Strip surrounding whitespaces
    code = code.strip()

    # Look up country code
    country = pycountry.countries.get(alpha_2=code)

    return code if country is None else country.name


def data2table(data: pandas.DataFrame, colors: list, title: Optional[str] = None) -> Table:
    """
    Creates 'rich' table from 'pandas' dataframe

    :param data: pandas.DataFrame Table data
    :param colors: list Column text colors
    :param title: str Table heading

    :return: rich.table.Table
    """

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
