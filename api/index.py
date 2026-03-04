"""Vercel Serverless Function entrypoint.

Vercel detects Python Serverless Functions from files inside the top-level
`api/` directory. We import the FastAPI app from `main.py`.
"""

from main import app  # noqa: F401
