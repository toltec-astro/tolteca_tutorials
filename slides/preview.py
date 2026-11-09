"""Serve the built slides (``_build/slides/``) on localhost."""

import sys
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

BUILD = Path(__file__).resolve().parents[1] / "_build/slides"
URL = "http://127.0.0.1:8951/index.html"


if __name__ == "__main__":
    if not (BUILD / "index.html").is_file():
        sys.exit(f"No slide build in {BUILD}; run `node slides/build-all.mjs` first.")
    print(URL, flush=True)
    ThreadingHTTPServer(
        ("127.0.0.1", 8951), partial(SimpleHTTPRequestHandler, directory=str(BUILD))
    ).serve_forever()
