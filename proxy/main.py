from typing import Union

from flask import Flask, request
from loguru import logger

from handlers.abstract import BaseHtmlHandler, BaseApiHandler
from handlers.all import get_handler

app = Flask(__name__)

def proxied_response(url: str) -> (str):
    """
    Get the response from destination url, redirect the navigation and assets
    through this server and munge in the additional bits we want (where a handler has
    been defined) before returning either:
    
    (a) a html str where it's a proxied web page.
    (b) a dict where its a proxied json response.
    """
    handler: Union[BaseHtmlHandler, BaseApiHandler, None] = get_handler(url)
    handler.logger = logger
    if handler:
        return handler.handle()
    else:
        return "No proxy handling for url: {url}", 404


@app.route("/")
def proxy():
    url = request.args.get("url", None)
    if not url:
        return "Invalid request. You need to include a url parameter.", 400
    return proxied_response(url)


if __name__ == "__main__":
    app.run(debug=True)
