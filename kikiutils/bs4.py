from bs4 import BeautifulSoup

# BS4

def get_bs4_soup(
    html: str | bytes,
    features: str = 'html.parser',
    from_encoding: str = 'utf-8',
    exclude_encodings: list[str] = ['utf-8'],
    **kwargs
):
    """Get bs4 soup object."""

    return BeautifulSoup(
        html,
        features,
        from_encoding = from_encoding,
        exclude_encodings = exclude_encodings,
        **kwargs
    )
