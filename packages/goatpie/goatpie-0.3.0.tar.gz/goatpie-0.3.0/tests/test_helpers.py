from goatpie.helpers import get_domain

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
    Tests 'get_domain'
    """

    # Assert result
    for url in domains:
        assert get_domain(url, True) == "example.com"

    for url in subdomains:
        assert get_domain(url, True) == "stats.example.com"


def test_get_domain_without_subdomain() -> None:
    """
    Tests 'get_domain'
    """

    # Assert result
    for url in domains + subdomains:
        assert get_domain(url, False) == "example.com"
