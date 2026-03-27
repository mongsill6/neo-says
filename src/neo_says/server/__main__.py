"""Run Neo Says API server.

Usage:
    python -m neo_says.server
"""

import uvicorn

from neo_says.server.app import app


def main():
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
