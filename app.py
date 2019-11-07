from flask import Flask, render_template, request, redirect, jsonify
from urllib.parse import urlparse
from werkzeug.exceptions import BadRequest, NotFound

from short_url import create_db, create_short_url, get_full_url, create_short_url

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/short", methods=["POST"])
def short():
    params = request.get_json(force=True, silent=True)
    if params is None or "url" not in params:
        raise BadRequest("No param 'url' in request data")

    url = params["url"]
    hostname = request.base_url.replace(urlparse(request.base_url).path, "")
    return jsonify({"url": f"{hostname}/u{create_short_url(url)}"})


@app.route("/u<short_url>", methods=["GET"])
def full(short_url):
    full_url = get_full_url(short_url)
    if full_url is None:
        raise NotFound()

    # https://stackoverflow.com/a/23343753
    if full_url.find("http://") != 0 and full_url.find("https://") != 0:
        full_url = "http://" + full_url
    return redirect(full_url, code=307)


if __name__ == "__main__":
    create_db()
    app.run()
