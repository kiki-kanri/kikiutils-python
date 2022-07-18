from bs4 import BeautifulSoup

# BS4

def get_bs4_soup(
    html: bytes | str,
    features: str = 'html.parser',
    exclude_encodings: list[str] = ['utf-8'],
    **kwargs
):
    """Get bs4 soup object."""

    return BeautifulSoup(
        html,
        features,
        exclude_encodings = exclude_encodings,
        **kwargs
    )
