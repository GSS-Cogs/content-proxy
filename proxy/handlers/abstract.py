from abc import ABCMeta, abstractmethod

from lxml.html import HtmlElement

from interventions.proxy import Proxier
from drivers import db

class AbstractHandler(metaclass=ABCMeta):

    def __init__(self, foreign_base_url):
        self.proxy = Proxier(foreign_base_url)
        self.db = db

    def proxy_page(self, content: HtmlElement, url: str) -> (HtmlElement):
        """
        Given _a_ url pattern on this site, do something then
        return some content.

        To be overwritten by individual page type handlers
        where one exists.

        Note: applied after self.proxy_site()
        """
        return content

    @abstractmethod
    def proxy_site(self, content: HtmlElement) -> (HtmlElement):
        """
        Given any content on this site url, do something then
        return some content.
        """
        pass
