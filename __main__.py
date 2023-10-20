from __future__ import annotations

import asyncio
import os

from dotenv import load_dotenv

from quart_app import app, runner

load_dotenv()

if os.environ.get("PRODUCTION") == "TRUE":
    PRODUCTION = True
elif os.environ.get("PRODUCTION") == "FALSE":
    PRODUCTION = False
else:
    raise ValueError("PRODUCTION environment variable not set")


if __name__ == "__main__":
    if PRODUCTION:
        asyncio.run(runner())
    else:
        app.run(debug=True)
