import os
from typing import Union

from flask import Flask, request
from loguru import logger
from lxml import html
import requests

import intervention
from intervention.handlers.abstract import AbstractHandler
from shim.rewriter import with_proxied_links

app = Flask(__name__)
app.logger = logger


def proxied_response(url: str) -> (str):
    """
    Get the response from destination url, redirect the navigation and assets
    through this server and munge in the additional bits we want (where a handler has
    been defined) before returning html.
    """
    r: requests.Response = requests.get(url)
    if not r.ok:
        raise Exception(f'Failed to get url, {url} with status code {r.status_code}')

    content: html.HtmlElement = html.document_fromstring(r.text)
    content = with_proxied_links(url, content)

    handler: Union[AbstractHandler, None] = intervention.get_handler(url)
    if handler:
        content = handler.handle(content)

    return html.tostring(content)

@app.route('/')
def proxy():
    url = request.args.get("url", None)
    if not url:
        return 'Invalid request. You need to include a url parameter.', 400
    return proxied_response(url)

if __name__ == "__main__":
    app.run(debug=True)