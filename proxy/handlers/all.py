from typing import Union

from .abstract import AbstractHandler
from .govuk import GovUKHandler, GovUKStatisticsHandler

# Note: ordering matters, partial paths below details paths please
handler_list = [
    ("https://www.gov.uk/government/statistics", GovUKStatisticsHandler),
    ("https://www.gov.uk", GovUKHandler),
]


def get_handler(url: str) -> (Union[None, AbstractHandler]):
    """
    Check the url pattern provided. Return a handler where
    one is found, else None.
    """
    for start_uri, handler in handler_list:
        if url.startswith(start_uri):
            foreign_base_url = "/".join(start_uri.split("/")[:3])
            return handler(foreign_base_url)
    return None
