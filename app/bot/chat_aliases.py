from __future__ import annotations

import logging
import re
from typing import Any

from app.config.settings import CHAT_ALIASES, OWNER_ID

logger = logging.getLogger(__name__)

_COMMANDS_WITH_CHAT_ID_FIRST = {
    "ddx",
    "mx1",
    "mx2",
    "joinx",
    "vx",
    "uv",
    "mx",
    "ximg",
    "vvv",
    "kingplay",
}

_COMMANDS_WITH_CHAT_ID_INLINE = {
    "xend",
}

_COMMAND_RE = re.compile(r"^/(?P<command>[a-zA-Z0-9_]+)(?:@\w+)?(?:\s|$)")


def _resolve_alias(value: str) -> str | None:
    alias = value.strip().lower()
    if not alias:
        return None

    chat_id = CHAT_ALIASES.get(alias)
    if chat_id is None:
        return None

    return str(chat_id)


def _rewrite_text(text: str) -> str:
    if not CHAT_ALIASES:
        return text

    lines = text.splitlines()
    if not lines:
        return text

    command_line = lines[0].strip()
    match = _COMMAND_RE.match(command_line)
    if not match:
        return text

    command = match.group("command").lower()

    if command in _COMMANDS_WITH_CHAT_ID_FIRST:
        if len(lines) < 2:
            return text

        resolved = _resolve_alias(lines[1])
        if resolved is None:
            return text

        lines[1] = resolved
        return "\n".join(lines)

    if command in _COMMANDS_WITH_CHAT_ID_INLINE:
        parts = command_line.split()
        if len(parts) < 2:
            return text

        alias_index = 2 if len(parts) >= 3 and parts[1].lower() == "pin" else 1
        if len(parts) <= alias_index:
            return text

        resolved = _resolve_alias(parts[alias_index])
        if resolved is None:
            return text

        parts[alias_index] = resolved
        lines[0] = " ".join(parts)
        return "\n".join(lines)

    return text


def preprocess_chat_aliases(update: Any) -> None:
    message = getattr(update, "message", None) or getattr(update, "edited_message", None)
    if not message:
        return

    from_user = getattr(message, "from_user", None)
    chat = getattr(message, "chat", None)
    if not from_user or not chat:
        return

    if getattr(from_user, "id", None) != OWNER_ID:
        return

    if getattr(chat, "type", None) != "private":
        return

    original_text = getattr(message, "text", None)
    if not original_text:
        return

    rewritten_text = _rewrite_text(original_text)
    if rewritten_text == original_text:
        return

    try:
        message.text = rewritten_text
    except Exception:
        object.__setattr__(message, "text", rewritten_text)

    logger.info(
        "CHAT_ALIAS_REWRITTEN | user_id=%s | message_id=%s",
        getattr(from_user, "id", None),
        getattr(message, "message_id", None),
    )
