from typing import NamedTuple, Optional


class ResourceMapped(NamedTuple):
    """
    A thing to identify the relationship between a
    given foreign landing page and our associated
    csvw resource.
    """

    landing_page: str
    csvw: str
