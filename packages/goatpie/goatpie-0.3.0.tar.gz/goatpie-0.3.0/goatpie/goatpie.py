import gzip
import io
import logging
import os
import sqlite3
import time
from logging.handlers import RotatingFileHandler
from typing import Optional

import arrow
import pandas
import pycountry
import requests

from .helpers import get_domain


class GoatPie:
    """
    'Goatcounter' analytics at your fingertips
    """

    # Base URL
    url: str = "https://example.goatcounter.com"

    # Request headers
    headers: dict = {"Content-type": "application/json"}

    # Request timeout (in seconds)
    timeout: int = 10

    # Database
    db: sqlite3.Connection

    # Minimum update interval (in seconds)
    interval: int = 1 * 60 * 60  # 1 hour

    def __init__(self, url: str, token: str, data_dir: str = ".tmp") -> None:
        """
        Creates 'GoatPie' instance

        :param url: str 'Goatcounter' instance URL
        :param token: str API token
        :param data_dir: str Data directory

        :return: None
        """

        # Store base URL
        self.url = url

        # Add API token
        self.headers["Authorization"] = f"Bearer {token}"

        # Store data directory
        self.data_dir = data_dir

        # Create data directory (if needed)
        os.makedirs(data_dir, exist_ok=True)

        # Initialize logger
        self.logger = self.get_logger(data_dir)

        # Connect to database
        db_file = os.path.join(data_dir, "db.sqlite")
        self.db = sqlite3.connect(db_file)

        # Populate database
        self.update()

    def fetch(self, endpoint: str, json: Optional[dict] = None) -> requests.Response:
        """
        Fetches data from 'Goatcounter' API

        :param endpoint: str API endpoint
        :param json: dict JSON body data

        :return: requests.Response
        """

        # If not specified ..
        if json is None:
            # .. assign default value
            json = {}

        # Prepare request
        # (1) Define HTTP method
        method = "post" if endpoint == "export" else "get"

        # (2) Build target URL
        base = f"{self.url}/api/v0/{endpoint}"

        # Call API
        return getattr(requests, method)(base, headers=self.headers, json=json, timeout=self.timeout)

    def export(self, first_id: int = 0) -> int:
        """
        Triggers generation of new export

        :param first_id: int Index of first entry

        :return: int Export identifier
        :throws: Exception Something went wrong
        """

        # Call API
        response = self.fetch("export", {"start_from_hit_id": first_id})

        # Get JSON response data
        data = response.json()

        # If error occurred ..
        if "error" in data:
            # .. report back
            raise Exception(data["error"])

        # Determine remaining API (= rate limit)
        remaining = response.headers["X-Rate-Limit-Remaining"]

        # If rate limit is (about to be) exceeded ..
        if int(remaining) < 2:
            # .. wait until next reset happens
            until_reset = response.headers["X-Rate-Limit-Reset"]

            # .. report back
            self.logger.info("Rate limit exceeded, waiting for reset in %s seconds ..", until_reset)

            # Bide the time
            time.sleep(int(until_reset))

        return data["id"]

    def status(self, idx: int) -> dict:
        """
        Checks progress of triggered export

        :param idx: int Export identifier

        :return: dict Status report
        """

        return self.fetch(f"export/{idx}").json()

    def download(self, idx: int) -> str:
        """
        Initiates download of finished export

        :param idx: int Export identifier

        :return: str Exported CSV data
        :throws: Exception Invalid response code
        """

        # Fetch archive
        response = self.fetch(f"export/{idx}/download")

        # If status code indicates error ..
        if response.status_code not in [200, 202]:
            # .. report back
            raise Exception(f"{response.status_code}: {response.content.decode('utf-8')}")

        # Unzip & stringify data
        return gzip.decompress(response.content).decode("utf-8")

    def update(self, last_update: int = 1 * 60 * 60) -> None:
        """
        Fetches analytics data & inserts it into local database

        :param last_update: int Minimum timespan since last update (in seconds)

        :return: None
        """

        # Define file containing next entry
        id_file = os.path.join(self.data_dir, ".next_idx")

        try:
            # If identifier file not present ..
            if not os.path.exists(id_file):
                # .. create it
                with open(id_file, "w", encoding="utf-8") as file:
                    file.write("0")

            # Get last modification & current time
            modified = arrow.get(os.path.getmtime(id_file))
            just_now = arrow.utcnow().to("local")

            # If time since last modification lesser than this ..
            if arrow.get(modified) > just_now.shift(seconds=-last_update):
                # .. do not update database (unless forced to)
                if last_update > 0:
                    # Get human-readable interval since last export
                    interval = arrow.get(modified).humanize()
                    feedback = interval if interval == "just now" else f"less than {interval}"

                    # Report back
                    raise Exception(f"Last update was {feedback}, skipping ..")

            # Append data if database table already exists
            if_exists = "append"

            # Attempt to ..
            try:
                # .. load identifier of next entry
                with open(id_file, "r", encoding="utf-8") as file:
                    first_id = int(file.read())

            # .. but if something goes south & table already exists ..
            except Exception:
                # .. replace it instead of appending to it
                if_exists = "replace"

            # Initiate data export & get export index
            idx = self.export(first_id or 0)

            # Enter indefinite loop
            while True:
                # Wait a ..
                time.sleep(1)

                # Receive export status
                status = self.status(idx)

                # Check export status
                if status["finished_at"] is None:
                    continue

                # If no new data available ..
                if status["num_rows"] == 0:
                    # .. store current time (preventing further requests)
                    timestamp = arrow.utcnow().to("local").timestamp()
                    os.utime(id_file, (timestamp, timestamp))

                    # .. report back
                    raise Exception("No new data, skipping ..")

                # Fetch string containing CSV data
                content = self.download(idx)

                # Load data into dataframe & store in database
                df = pandas.read_csv(io.StringIO(content))
                df.to_sql("data", self.db, if_exists=if_exists, index=False)

                # Update identifier of last entry
                with open(id_file, "w", encoding="utf-8") as file:
                    file.write(str(int(status["last_hit_id"]) + 1))

                # Step out of the loop
                break

        except Exception:
            # Capture stack trace
            self.logger.exception("Something went wrong")

    def execute(self, command: str, params: Optional[dict] = None) -> pandas.DataFrame:
        """
        Executes SQL command against database

        :param command: str SQL command
        :param params: str Query parameters

        :return: pandas.DataFrame
        :throws: Exception Something went wrong
        """

        try:
            return pandas.read_sql(command, self.db, params=params)

        except Exception:
            # Capture stack trace
            self.logger.exception("Something went wrong")

            # Reraise exception
            raise

    def get_referrers(self, limit: int = 12) -> pandas.DataFrame:
        """
        Provides (limited set of) most commonly used referrers

        :param limit: int Limits data to last XY entries

        :return: pandas.DataFrame
        """

        # Load dataframe from database
        # (1) No bots
        # (2) Group by referrer
        # (3) Sort by count
        referrers = self.execute(
            """
            SELECT count(Referrer) as Total, Referrer
            FROM data
            WHERE Bot == 0
            GROUP BY Referrer
            ORDER BY Total DESC
            """
        )

        # Filter out internal links
        # (1) Convert entries to strings (prevent 'None' causing problems)
        referrers["Referrer"] = referrers["Referrer"].astype(str)

        # (2) Remove entries containing domain being used
        referrers = referrers[~referrers["Referrer"].str.contains(get_domain(self.url))]

        # Add percentages
        referrers["%"] = round(referrers["Total"] / referrers["Total"].sum() * 100, 1)

        return referrers.head(limit)

    def get_pages(self, limit: int = 12) -> pandas.DataFrame:
        """
        Provides (limited set of) most commonly visited pages

        :param limit: int Limits data to last XY entries

        :return: pandas.DataFrame
        """

        # Load dataframe from database
        # (1) No bots
        # (2) Group by path
        # (3) Sort by count
        # (4) Last XY entries
        pages = self.execute(
            """
            SELECT count("2Path") as Total, "2Path" as Page
            FROM data
            WHERE Bot == 0
            GROUP BY Page
            ORDER BY Total DESC
            """
        )

        # Add percentages
        pages["%"] = round(pages["Total"] / pages["Total"].sum() * 100, 1)

        return pages.head(limit)

    def get_browsers(self, limit: int = 12) -> pandas.DataFrame:
        """
        Provides (limited set of) most commonly used browsers

        :param limit: int Limits data to last XY entries

        :return: pandas.DataFrame
        """

        # Load dataframe from database
        # (1) No bots
        # (2) Group by browser
        # (3) Sort by count
        # (4) Last XY entries
        browsers = self.execute(
            """
            SELECT count(Browser) as Total, Browser
            FROM data
            WHERE Bot == 0
            GROUP BY Browser
            ORDER BY Total DESC
            """
        )

        # Add percentages
        browsers["%"] = round(browsers["Total"] / browsers["Total"].sum() * 100, 1)

        return browsers.head(limit)

    def get_systems(self, limit: int = 12) -> pandas.DataFrame:
        """
        Provides (limited set of) most commonly used operating systems

        :param limit: int Limits data to last XY entries

        :return: pandas.DataFrame
        """

        # Load dataframe from database
        # (1) No bots
        # (2) Group by system
        # (3) Sort by count
        systems = self.execute(
            """
            SELECT count(System) as Total, System
            FROM data
            WHERE Bot == 0
            GROUP BY System
            ORDER BY Total DESC
            """
        )

        # Add percentages
        systems["%"] = round(systems["Total"] / systems["Total"].sum() * 100, 1)

        return systems.head(limit)

    def get_pageviews(self, limit: int = 14) -> pandas.DataFrame:
        """
        Provides (limited set of) pageviews (= total hits) per day

        :param limit: int Limits data to last XY days

        :return: pandas.DataFrame
        """

        # Load dataframe from database
        # (1) No bots
        # (2) Group by day
        # (3) Sort by day
        pageviews = self.execute(
            """
            SELECT strftime("%Y-%m-%d", Date) as Day, count(*) as Pageviews
            FROM data
            WHERE Bot == 0
            GROUP BY Day
            ORDER BY Day DESC
            """
        )

        return pageviews.head(limit)

    def get_visits(self, limit: int = 14) -> pandas.DataFrame:
        """
        Provides (limited set of) visits (= unique users) per day

        :param limit: int Limits data to last XY days

        :return: pandas.DataFrame
        """

        # Load dataframe from database
        # (1) No bots
        # (2) Group by day
        # (3) Sort by day
        visits = self.execute(
            """
            SELECT strftime("%Y-%m-%d", Date) as Day, count(distinct Session) as Visits
            FROM data
            WHERE Bot == 0
            GROUP BY Day
            ORDER BY Day DESC
            """
        )

        return visits.head(limit)

    def get_devices(self) -> pandas.DataFrame:
        """
        Provides device types (according to screen sizes)

        :return: pandas.DataFrame
        """

        # Load dataframe from database
        # (1) No bots
        # (2) Group by screen size
        devices = self.execute(
            """
            SELECT count("Screen size") as Total, "Screen size" as Device
            FROM data
            WHERE Bot == 0
            GROUP BY Device
            """
        )

        # Replace screen size with device type
        devices["Device"] = devices["Device"].map(self.get_device)

        # Group device types & aggregate their totals
        devices = devices.groupby("Device").agg({"Total": sum, "Device": "first"})

        # Add percentages
        devices["%"] = round(devices["Total"] / devices["Total"].sum() * 100, 1)

        # Sort by count
        return devices.sort_values(by="Total", ascending=False)

    def get_countries(self, limit: int = 12) -> pandas.DataFrame:
        """
        Provides (limited set of) most common countries

        :param limit: int Limits data to last XY entries

        :return: pandas.DataFrame
        """

        # Load dataframe from database
        # (1) No bots
        # (2) Group by country
        # (3) Sort by count
        countries = self.execute(
            """
            SELECT count(Location) as Total, Location as Country
            FROM data
            WHERE Bot == 0
            GROUP BY Location
            ORDER BY Total DESC
            """
        )

        # Replace country codes with actual country names
        # (1) Convert entries to strings (prevent 'None' causing problems)
        countries["Country"] = countries["Country"].astype(str)

        # (2) Replace entries
        countries["Country"] = countries["Country"].map(self.get_country)

        # Add percentages
        countries["%"] = round(countries["Total"] / countries["Total"].sum() * 100, 1)

        return countries.head(limit)

    # Helper functions

    def get_logger(self, log_dir: str) -> logging.Logger:
        """
        Initializes logger

        :param log_dir: str Path to logfile

        :return: logging.Logger
        """

        # Initialize logger & set logging level
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)

        # Create handler
        handler = RotatingFileHandler(os.path.join(log_dir, "debug.log"), maxBytes=10000)

        # Format logfile content
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        handler.setFormatter(formatter)

        # Add handler to logger
        logger.addHandler(handler)

        return logger

    def get_device(self, size: str) -> str:
        """
        Converts screen size to device type (if applicable)

        :param size: str Screen size (w,h,dpi)

        :return: str Device type (if matched), otherwise 'unknown'
        """

        # Strip whitespaces
        size = size.strip()

        # If size undefined ..
        if not size:
            # .. assign zero ('unknown device')
            size = 0

        # Determine largest value (width OR height)
        size = int(max(size.split(",")))

        # Map screen size to device type
        if size > 3000:
            return "Computer monitors larger than HD"

        if size > 1920:
            return "Computer monitors"

        if size > 1100:
            return "Tablets and small laptops"

        if size > 1000:
            return "Large phones, small tablets"

        if size > 300:
            return "Phones"

        return "Unknown devices"

    def get_country(self, code: str) -> str:
        """
        Converts country code to country name (if applicable)

        :param code: str Country code

        :return: str Country name (if successful), otherwise country code
        """

        # Look up country code
        country = pycountry.countries.get(alpha_2=code)

        return code if country is None else country.name
