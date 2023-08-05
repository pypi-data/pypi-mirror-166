from pandas import DataFrame
from rich.table import Table

from goatpie.helpers import data2table, get_country, get_device, get_domain

# Global setup
# (1) Domains
domains = [
    "example.com",
    "//example.com",
    "\\example.com",
    "http://example.com",
    "https://example.com",
    "https://example.com",
    "https://example.com/stats",
    "https://example.com/?stats=1",
]

# (2) Subdomains
subdomains = [
    "stats.example.com",
    "//stats.example.com",
    "\\stats.example.com",
    "http://stats.example.com",
    "https://stats.example.com",
    "https://stats.example.com",
    "https://stats.example.com/stats",
    "https://stats.example.com/?stats=1",
]


def test_get_domain_with_subdomain() -> None:
    """
    Tests 'get_domain' (keeping subdomain)
    """

    # Assert result
    for url in domains:
        assert get_domain(url, True) == "example.com"

    for url in subdomains:
        assert get_domain(url, True) == "stats.example.com"


def test_get_domain_without_subdomain() -> None:
    """
    Tests 'get_domain' (removing subdomain)
    """

    # Assert result
    for url in domains + subdomains:
        assert get_domain(url, False) == "example.com"


def test_get_country() -> None:
    """
    Tests 'get_country'
    """

    # Assert result
    assert get_country("DE") == "Germany"


def test_get_country_invalid() -> None:
    """
    Tests 'get_country' (invalid 'code')
    """

    # Assert result #1
    assert get_country("") == ""

    # Assert result #2
    assert get_country("XY") == "XY"


def test_get_device() -> None:
    """
    Tests 'get_device'
    """

    # Assert result #1
    for i in range(300, 1000):
        assert get_device(str(i)) == "Phones"

    # Assert result #2
    for i in range(1000, 1100):
        assert get_device(str(i)) == "Large phones, small tablets"

    # Assert result #3
    for i in range(1100, 1920):
        assert get_device(str(i)) == "Tablets and small laptops"

    # Assert result #4
    for i in range(1920, 3000):
        assert get_device(str(i)) == "Computer monitors"

    # Assert result #5
    for i in range(3000, 5000):
        assert get_device(str(i)) == "Computer monitors larger than HD"


def test_get_device_order() -> None:
    """
    Tests 'get_device' (different order, same result)
    """

    # Assert result #1
    assert get_device("480") == "Phones"

    # Assert result #2
    assert get_device("320,480") == "Phones"

    # Assert result #3
    assert get_device("480,320") == "Phones"

    # Assert result #4
    assert get_device("480,320,1") == "Phones"


def test_get_device_invalid() -> None:
    """
    Tests 'get_device' (invalid 'size')
    """

    # Assert result #1
    assert get_device("") == "Unknown devices"

    # Assert result #3
    assert get_device("120") == "Unknown devices"

    # Assert result #2
    assert get_device("pine64") == "Unknown devices"


def test_data2table():
    """
    Tests 'data2table'
    """

    # Setup
    # (1) Data table
    data = DataFrame.from_dict({"c1": ["a", "b"], "c2": ["c", "d"]})

    # Run function
    table = data2table(data, ["blue", "blue"])

    # Assert result
    assert isinstance(table, Table)
