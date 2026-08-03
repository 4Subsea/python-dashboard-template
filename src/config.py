"""Everything that differs between a laptop, the server and CI.

Values come from the environment, falling back to the defaults below - so a
fresh clone runs with no setup and CI needs no configuration. To override,
copy `.env.example` to `.env` in the repo root and edit it; `.env` is
gitignored, so your local paths never reach anyone else's machine.

"""

import os
import pathlib

from dotenv import load_dotenv

# The repo root, found from this file rather than the working directory
ROOT = pathlib.Path(__file__).resolve().parents[1]

# Load enviroment variables from env file. override=False means  a variable already set in the real environment wins over the
# file
load_dotenv(ROOT / ".env", override=False)

# ---------------------------------------------------------------------------
# Store environment variables in globals
# ---------------------------------------------------------------------------
DASH_DEBUG = os.getenv("DASH_DEBUG", "true").strip().lower() == "true"
DASH_HOST = os.getenv("DASH_HOST", "127.0.0.1")
DASH_PORT = int(os.getenv("DASH_PORT") or 8050)
MOCK_PLATFORM_CHROME = int(os.getenv("MOCK_PLATFORM_CHROME", "0") or 0)
MOCK_PLATFORM_GAP = int(os.getenv("MOCK_PLATFORM_GAP", "24") or 24)


def summary():
    """Every setting and its value, for `python src/config.py`.

    Useful on the server: it answers "what does the app think it is reading?"
    without starting it.
    """
    return {
        name: value
        for name, value in sorted(globals().items())
        if name.isupper() and not name.startswith("_")
    }


if __name__ == "__main__":
    print(f"repo root: {ROOT}")
    print(f".env:      {'found' if (ROOT / '.env').exists() else 'not present, using defaults'}\n")
    for name, value in summary().items():
        print(f"  {name:<24}{value}")
