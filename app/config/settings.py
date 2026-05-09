from __future__ import annotations

import json
import os
from pathlib import Path

# ========================
# BASE
# ========================

BASE_DIR = Path(__file__).resolve().parents[2]

# ========================
# TELEGRAM
# ========================

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")


def _int_env(name: str, default: int) -> int:
    value = os.getenv(name, "").strip()
    if not value:
        return default
    try:
        return int(value)
    except ValueError:
        return default


OWNER_ID = _int_env("OWNER_ID", 8505890439)


def _chat_aliases_env() -> dict[str, int]:
    raw = os.getenv("CHAT_ALIASES", "").strip()
    if not raw:
        return {}

    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return {}

    if not isinstance(data, dict):
        return {}

    aliases: dict[str, int] = {}
    for key, value in data.items():
        alias = str(key).strip().lower()
        if not alias:
            continue
        if not alias.replace("_", "").replace("-", "").isalnum():
            continue
        try:
            aliases[alias] = int(value)
        except (TypeError, ValueError):
            continue

    return aliases


CHAT_ALIASES = _chat_aliases_env()

# ========================
# SPOTIFY
# ========================

SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID", "")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET", "")

BASE_URL = os.getenv("BASE_URL", "http://localhost:8000").rstrip("/")
SPOTIFY_REDIRECT_URI = f"{BASE_URL}/callback"

SPOTIFY_SCOPES = "user-read-currently-playing user-read-recently-played"

# ========================
# PERFORMANCE
# ========================

SPOTIFY_HTTP_TIMEOUT_SECONDS = float(os.getenv("SPOTIFY_HTTP_TIMEOUT_SECONDS", "10"))
SPOTIFY_MAX_CONCURRENT_REQUESTS = int(os.getenv("SPOTIFY_MAX_CONCURRENT_REQUESTS", "10"))

SPOTIFY_CACHE_TTL_SECONDS = float(os.getenv("SPOTIFY_CACHE_TTL_SECONDS", "5"))
SPOTIFY_CACHE_MAX_ENTRIES = int(os.getenv("SPOTIFY_CACHE_MAX_ENTRIES", "500"))

SPOTIFY_PER_USER_RATE_LIMIT = int(os.getenv("SPOTIFY_PER_USER_RATE_LIMIT", "10"))
SPOTIFY_RATE_LIMIT_WINDOW_SECONDS = float(os.getenv("SPOTIFY_RATE_LIMIT_WINDOW_SECONDS", "5"))

SPOTIFY_CIRCUIT_BREAKER_THRESHOLD = int(os.getenv("SPOTIFY_CIRCUIT_BREAKER_THRESHOLD", "3"))
SPOTIFY_CIRCUIT_BREAKER_COOLDOWN_SECONDS = float(
    os.getenv("SPOTIFY_CIRCUIT_BREAKER_COOLDOWN_SECONDS", "8")
)

# ========================
# DATABASE (FIXED SQLITE + VOLUME)
# ========================

DATA_DIR = Path("/data")
DATA_DIR.mkdir(parents=True, exist_ok=True)

DATABASE_URL = os.getenv("DATABASE_URL", "").strip()

if not DATABASE_URL:
    DATABASE_URL = f"sqlite:///{DATA_DIR / 'app.db'}"