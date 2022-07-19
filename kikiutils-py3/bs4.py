from bs4 import BeautifulSoup
from typing import Union

# BS4

def get_bs4_soup(
    html: Union[bytes, str],
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
