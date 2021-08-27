from typing import Union

from .abstract import BaseHtmlHandler, BaseApiHandler
from .govuk import GovUKHandler, GovUKStatisticsHandler, GovUKApiContentHandler

# Note: ordering matters, partial paths below details paths please
handler_list = [
    ("https://www.gov.uk/government/statistics", GovUKStatisticsHandler),
    ("https://www.gov.uk/api/content", GovUKApiContentHandler),
    ("https://www.gov.uk", GovUKHandler),
]


def get_handler(url: str) -> (Union[None, BaseHtmlHandler, BaseApiHandler]):
    """
    Check the url pattern provided. Return a handler where
    one is found, else None.
    """
    for start_uri, handler in handler_list:
        if url.startswith(start_uri):
            return handler(url)
    return None
