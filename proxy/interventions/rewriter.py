import os
from typing import NamedTuple

from lxml import html

""" Instantiates a ReWriter class which wraps the Modifer and Inserter classes to allow on the fly modification of html"""


class Modifier:
    """Class for modifying lxml.HtmlElement objects."""

    def __init__(self):
        pass

    def attribute(
        self, element: html.HtmlElement, attribute_name: str, operation: callable
    ) -> (html.HtmlElement):
        """Update one attribute of one element using the callable"""
        new_attribute_value = operation(element.get(attribute_name))
        element.set(attribute_name, new_attribute_value)
        return element

class ReWriter(NamedTuple):
    modify = Modifier()
