from lxml import html
from flask import Flask, request
import os

from requests import Response as RequestReponse # there a flask.Response class we may need later
import requests

app = Flask(__name__)

SHIM_ROOT = os.environ.get("SHIM_ROOT", 'http://127.0.0.1:5000/')

def with_proxied_navigation(html_as_str, url):
    """
    Prefix all <a> href= links with with our proxy url
    to sustain the shim.
    """
    url_root = "/".join(url.split("/")[:3])
    html_as_str = html_as_str.replace('href="/', f'href="{SHIM_ROOT}?url={url_root}/')
    return html_as_str

def proxied_response(url: str):
    """
    Get the response from from destination url, and munge in
    the additional bits we want. 
    """
    r: RequestReponse

    r = requests.get(url)
    if not r.ok:
        raise Exception(f'Failed to get url, {url} with status code {r.status_code}')

    content = html.document_fromstring(with_proxied_navigation(r.text, url))

    return html.tostring(content)

@app.route('/')
def proxy():
    url = request.args.get("url", None)
    if not url:
        return 'Invalid request. You need to include a url parameter.', 400
    return proxied_response(url)

if __name__ == "__main__":
    app.run()