"""
Helpers for building public-facing URLs.
"""

from ipaddress import ip_address
from urllib.parse import urlparse

from app.core.config import get_config


def _is_loopback_host(host: str) -> bool:
    value = str(host or "").strip().strip("[]").lower()
    if not value:
        return False
    if value in {"localhost", "0.0.0.0"}:
        return True
    try:
        parsed = ip_address(value)
    except ValueError:
        return False
    return parsed.is_loopback or parsed.is_unspecified


def get_public_app_url() -> str:
    app_url = str(get_config("app.app_url") or "").strip().rstrip("/")
    if not app_url:
        return ""
    try:
        parsed = urlparse(app_url)
    except Exception:
        return ""
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        return ""
    if _is_loopback_host(parsed.hostname or ""):
        return ""
    return app_url


def build_public_file_url(path: str) -> str:
    raw_path = str(path or "").strip()
    if not raw_path:
        return ""
    if not raw_path.startswith("/"):
        raw_path = f"/{raw_path}"
    app_url = get_public_app_url()
    if app_url:
        return f"{app_url}{raw_path}"
    return raw_path
