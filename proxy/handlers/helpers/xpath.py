import copy

from lxml import html
from lxml.html import HtmlElement

""" Wrap some common xpath based functions for reuse """

def _prettify(issue: str, element: HtmlElement):
    """
    Given an issue and the element the issue is with. Give
    the user something they can debug.
    """
    return (f'''
{issue}:

{html.tostring(element, pretty_print=True).decode()}
    ''')

def assert_get_one(element: HtmlElement, xpath_statement: str):
    """
    Given an HtmlElement and an xpath statement, confirm the statement selects
    exactly one element then return it as a singleton.
    """
    elements = element.xpath(xpath_statement)
    assert len(elements) == 1, _prettify(f'\nExpecting 1 element using xpath "{xpath_statement}", got {len(elements)} from:', element)
    return elements[0]

def first_element_matching(element: HtmlElement, xpath_statement: str):
    """
    Given an HtmlElement and an xpath statement, confirm the statement selects
    at least one elementm then return the first element.
    """
    elements = element.xpath(xpath_statement)
    assert len(elements) > 0, _prettify(f'\nExpecting at least 1 element using xpath "{xpath_statement}", got 0 from:', element)
    return elements[0]


def copy_first_element_matching(element: HtmlElement, xpath_statement: str):
    """
    Given an HtmlElement and an xpath statement, deepcopy the first
    element that matches the statment.
    """
    elements = element.xpath(xpath_statement)
    assert len(elements) > 0
    return copy.deepcopy(elements[0])
