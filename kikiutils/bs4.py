from bs4 import BeautifulSoup

# BS4

def get_bs4_soup(html: str | bytes, features: str = 'html.parser', **kwargs):
    """Get bs4 soup object."""

    return BeautifulSoup(html, features, **kwargs)
