from typing import Union

from intervention.handlers.abstract import AbstractHandler
from intervention.handlers.govuk import GovUKStatisticsHandler

handler_list = [
    ("https://www.gov.uk/government/statistics", GovUKStatisticsHandler)
]

def get_handler(url: str) -> (Union[None, AbstractHandler]):
    """
    Check the url pattern provided. Return a handler where
    one is found, else None.
    """
    for start_uri, handler in handler_list:
        if url.startswith(start_uri):
            return handler()
    return None
    
