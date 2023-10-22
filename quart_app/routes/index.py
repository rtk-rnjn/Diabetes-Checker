from __future__ import annotations

from quart import render_template, request

from quart_app.app import app, ml
from utils import get_data


@app.route("/", methods=["GET"])
async def req():
    if not request.args:
        return await render_template("index.html")

    data = get_data(request)
    r = await ml.try_cache(**data) or await ml.predict(**data)

    if r:
        temp = "You are at risk of diabetes"
        cls = "danger"
    else:
        temp = "You are not at risk of diabetes"
        cls = "success"

    return await render_template("index.html", result=temp, cls=cls)
