from abc import ABCMeta, abstractmethod

from lxml import html
import requests

from interventions.proxy import Proxier
from drivers import db

class BaseHtmlHandler(metaclass=ABCMeta):

    def __init__(self, url):
        foreign_base_url = "/".join(url.split("/")[:3])
        self.proxy = Proxier(foreign_base_url)
        self.db = db
        self.logger = None # TODO - what if the is called but none?

        r: requests.Response = requests.get(url)
        if not r.ok:
            raise Exception(f"Failed to get url, {url} with status code {r.status_code}")

        self.content: html.HtmlElement = html.document_fromstring(r.text)
        self.url = url

    def handle(self):
        content = self.proxy_site(self.content)
        content = self.proxy_page(content, self.url)
        return html.tostring(content)


    def proxy_page(self, content: html.HtmlElement, url: str) -> (html.HtmlElement):
        """
        Given _a_ url pattern on this site, do something then
        return some content.

        To be overwritten by individual page type handlers
        where one exists.

        Note: applied after self.proxy_site()
        """
        return content

    @abstractmethod
    def proxy_site(self, content: html.HtmlElement) -> (html.HtmlElement):
        """
        Given any html content, do something to it then
        return that html content.
        """
        pass


class BaseApiHandler(metaclass=ABCMeta):
    
    def __init__(self, url):
        foreign_base_url = "/".join(url.split("/")[:3])
        self.proxy = Proxier(foreign_base_url)
        self.db = db

        # TODO - what if the is called but none?
        self.logger = None
        self.url = url

    def handle(self):
        return self.proxy_api(self.url)
    
    @abstractmethod
    def proxy_api(self, url: str) -> (dict):
        """
        Given a document at this url, do something to it then
        return that document.
        """
        pass