from __future__ import annotations

from hypercorn.asyncio import serve
from hypercorn.config import Config

from .app import app

config = Config()
config.bind = ["0.0.0.0:6969"]
config.loglevel = "INFO"
config.accesslog = "-"
config.errorlog = "-"
config.use_reloader = True


def runner():
    return serve(app, config)
