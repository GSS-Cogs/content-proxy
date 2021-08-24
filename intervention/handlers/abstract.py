from abc import ABCMeta, abstractmethod

from lxml.html import HtmlElement

class AbstractHandler(metaclass=ABCMeta):

    @abstractmethod
    def handle(self, content: HtmlElement) -> (HtmlElement):
        """
        Given some content, do something then
        return some content. 
        """
