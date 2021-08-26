import os

from lxml import html

from .rewriter import ReWriter

PROXY_ROOT = os.environ.get("PROXY_ROOT", "http://127.0.0.1:5000")


class Proxier:
    """
    Proxy class to factor out the common html intervetions required to
    create a proxied view of a web page. 
    """

    def __init__(self, foreign_base_url):
        self.new_root = PROXY_ROOT
        self.rewriter = ReWriter()
        self.foreign_base_url = foreign_base_url

    def get_foreign_base(self):
        """
        Police that the user has set a base url for the site being shimmed before calling
        methods that will require this knowledge.
        """
        if not self.foreign_base_url:
            raise Exception('To make this modification, you need to first specify the base url of the site whose html you are modifying.')
        return self.foreign_base_url

    def all_relative_to_absolute_href_of_a(self, element: html.HtmlElement):
        """
        Updates the href attribute of all child elements of <a> to use absolute paths
        proxied through this server.
        """
        for child_element in element.xpath("//a"):
            child_element = self.relative_to_absolute_proxied(child_element, "href")
        return element

    def all_relative_to_absolute_href_of_link_css(self, element: html.HtmlElement):
        """
        Updates each attribute of all child <link> elements with an href
        attribute ending in .css to be absolute paths.
        """
        for child_element in element.xpath("//link"):
            if not child_element.get('href', '').endswith(".css"):
                continue
            child_element = self.relative_to_absolute(child_element, "href")
        return element

    def all_relative_to_absolute_srcset_of_img(self, element: html.HtmlElement):
        """
        Updates each path with a srcset attribute of each child <img> element to be absolute
        not relative.
        """
        for child_element in element.xpath('//img'):
            if child_element.get('srcset', None):
                child_element = self.relative_to_absolute_srcset(child_element)
        return element

    def all_relative_to_absolute_src_of_img(self, element: html.HtmlElement):
        """
        Updates the src attribute of each child <img> element to be absolute
        not relative.
        """
        for child_element in element.xpath('//img'):
            if child_element.get('src', None):
                child_element = self.relative_to_absolute(child_element, "src")
        return element

    def all_relative_to_absolute_script_js(self, element: html.HtmlElement):
        """
        Updates each js src attribute within each <script> element to be an absolute
        not relative path.
        """
        for child_element in element.xpath('//script'):
            if child_element.get('src', '').endswith('.js'):
                child_element = self.relative_to_absolute(child_element, "src")
        return element

    def relative_to_absolute(self, element: html.HtmlElement, attribute: str) -> (html.HtmlElement):
        """
        Updates a attribute of an element to be an absolute path where that attributes
        value starts with "/".
        """
        return self.rewriter.modify.attribute(
            element,
            attribute,
            lambda x: f"{self.get_foreign_base()}{x}" if x.startswith("/") else x,
        )

    def relative_to_absolute_proxied(self, element: html.HtmlElement, attribute: str) -> (html.HtmlElement):
        """
        Updates a attribute of an element to be an absolute path proxied through this
        server where that attributes value starts with "/".
        """
        return self.rewriter.modify.attribute(
            element,
            attribute,
            lambda x: f"{self.new_root}/?url={self.get_foreign_base()}{x}" if x.startswith("/") else x
        )

    def relative_to_absolute_srcset(self, element: html.HtmlElement):
        """
        Updates a srcset element so each entry uses absolute not relative paths.
        """
        def update_srcset(srcset_attribute_value):
            srcs = srcset_attribute_value.split(",")
            srcs = [f"{self.get_foreign_base()}{x}" for x in srcs]
            return ",".join(srcs)

        return self.rewriter.modify.attribute(
            element,
            "srcset",
            update_srcset
        )
