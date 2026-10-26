"""Explicit Vercel Function entry point for the Flask application."""

import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from main2 import app as flask_app


class VercelPathFix:
    """Strip Vercel rewrite prefix so Flask routing sees the real path.

    Handles /api/index, /api/index.py, /api/index/..., and /api/index.py/...
    so routes and static assets resolve correctly on Vercel.
    """

    def __init__(self, app):
        self.app = app

    @staticmethod
    def clean_path(raw_path: str) -> str:
        if not raw_path:
            return "/"

        # Strip query string
        path = raw_path.split("?")[0].strip()

        # Strip serverless script prefixes
        for prefix in ("/api/index.py", "/api/index"):
            if path == prefix or path == prefix + "/":
                return "/"
            if path.startswith(prefix + "/"):
                path = path[len(prefix):]
                break

        if not path or path == "":
            return "/"
        if not path.startswith("/"):
            path = "/" + path

        return path

    def __call__(self, environ, start_response):
        # Reset SCRIPT_NAME to prevent Werkzeug routing prefix mismatch
        environ["SCRIPT_NAME"] = ""

        # Check edge headers or PATH_INFO
        raw_path = environ.get("PATH_INFO") or ""
        if not raw_path or raw_path in ("/api/index", "/api/index.py", "/api/index/", "/api/index.py/"):
            edge_path = (
                environ.get("HTTP_X_FORWARDED_PATH")
                or environ.get("HTTP_X_NOW_ROUTE_URI")
                or environ.get("REQUEST_URI")
                or environ.get("RAW_URI")
            )
            if edge_path:
                raw_path = edge_path

        cleaned = self.clean_path(raw_path)
        environ["PATH_INFO"] = cleaned
        return self.app(environ, start_response)


app = VercelPathFix(flask_app)
