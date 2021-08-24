from intervention.handlers.abstract import AbstractHandler

from lxml.html import HtmlElement

class GovUKStatisticsHandler(AbstractHandler):
    """
    handles urls beginning: https://www.gov.uk/government/statistics
    """

    def handle(self, content: HtmlElement) -> (HtmlElement):
        return content