import logging
import os
import urllib.parse
import requests
import urllib

from flask import Flask
from flask import request
from flask import make_response, redirect

app = Flask(__name__)

website = "https://www.vpngate.net"

@app.route('/')
def root():
    return index('/')

@app.route('/<path:subpath>')
def index(subpath):

    upstream_url = urllib.parse.urljoin(website, subpath)

    resp = requests.request(method=request.method, url=upstream_url,data=request.get_data(),  allow_redirects=False)

    if resp.status_code == 302:
        location = resp.headers.get("Location")
        if location:
            return redirect(location, code=302)
        else:
            return make_response("302 without Location header", 500)

    app.logger.info("%s - \"%s %s %s\" %s", request.remote_addr, request.method, request.query_string, request.scheme, resp.status_code)
    
    headers = {
        "Content-Type": resp.headers.get("Content-Type", "text/html"),
        "Content-Length": resp.headers.get("Content-Length", "0"),
    }
    return make_response((resp.content, resp.status_code, headers))

