import os
from lxml import html

"""
This is fairly nasty, you can't write back to an html.HtmlElement etree so (for now) we're:

* finding the html that needs replacing with xpath
* creating a replacement dict
* converting the _whole_ html.HtmlElement to str -> replacing -> back to html.HtmlElement

May need something better than this if we're in it for the longer term.
"""

SHIM_ROOT = os.environ.get('SHIM_ROOT', 'http://127.0.0.1:5000/')

def make_replacements(content: html.HtmlElement, replacements:dict) -> (html.HtmlElement):
    """
    Given a dictionary of replacements in the form {str_to_replace: replace_with_this_str}
    switch out the old strings with our modified version. 
    """
    html_as_str = html.tostring(content).decode('utf-8')
    for replace_me, with_me in replacements.items():
        html_as_str = html_as_str.replace(replace_me, with_me)
    return html.fromstring(html_as_str)


def with_proxied_links(url: str, content: html.HtmlElement) -> (html.HtmlElement):
    """
    Prefix all navigation and assets links to sustain the shim.
    """
    url_root = "/".join(url.split("/")[:3])
    
    def replace_navigation(element: html.HtmlElement):
        element_html = html.tostring(element).decode('utf-8')
        element_html_replaced = element_html.replace('href="/', f'href="{SHIM_ROOT}?url={url_root}/')
        return {element_html: element_html_replaced}

    def replace_css_assets(element: html.HtmlElement):
        element_html = html.tostring(element).decode('utf-8')
        element_html_replaced = None
        tokens = element_html.split(" ")
        css_asset = [x for x in tokens if 'href="/assets' in x and ".css" in x]
        if len(css_asset) == 1:
            element_html_replaced = element_html.replace('href="/', f'href="{url_root}/')
            return {element_html: element_html_replaced}
        return None

    def replace_js_assets(element: html.HtmlElement):
        element_html = html.tostring(element).decode('utf-8')
        element_html_replaced = None
        element_html_replaced = element_html.replace('="/assets', f'{url_root}/assets')
        if element_html_replaced:
            return {element_html: element_html_replaced}
        return None

    def replace_image_assets(element: html.HtmlElement):
        element_html = html.tostring(element).decode('utf-8')
        element_html_replaced = None
        element_html_replaced = element_html.replace('/assets', f'{url_root}/assets')
        if element_html_replaced:
            return {element_html: element_html_replaced}
        return None

    # Navigation
    replacements = {}
    for element in content.xpath('//a'):
        replacements.update(replace_navigation(element))
    content = make_replacements(content, replacements)

    # css
    replacements = {}
    for element in content.xpath('//link'):
        css_replaced = replace_css_assets(element)
        if css_replaced:
            replacements.update(css_replaced)
    content = make_replacements(content, replacements)

    # js
    replacements = {}
    for element in content.xpath('//script'):
        js_replaced = replace_js_assets(element)
        if js_replaced:
            replacements.update(js_replaced)
    content = make_replacements(content, replacements)

    # images
    replacements = {}
    for element in content.xpath('//img'):
        img_replaced = replace_image_assets(element)
        if img_replaced:
            replacements.update(img_replaced)
    content = make_replacements(content, replacements)

    return content