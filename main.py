from __future__ import annotations

import asyncio
import os

from dotenv import load_dotenv

from quart_app import app, runner

load_dotenv()

if __name__ == "__main__":
    asyncio.run(runner())
