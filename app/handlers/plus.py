from __future__ import annotations

import logging

from aiogram import Bot, Router, types
from aiogram.filters import Command

from app.config.settings import OWNER_ID

router = Router()
logger = logging.getLogger(__name__)


def parse_payload(text: str | None) -> tuple[int | None, str | None]:
    if not text:
        return None, None

    try:
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        chat_id = int(lines[1])
        user_raw = lines[2]
        return chat_id, user_raw
    except Exception:
        return None, None


async def resolve_user(bot: Bot, user_raw: str) -> int | None:
    if user_raw.isdigit():
        return int(user_raw)

    if user_raw.startswith("@"):
        try:
            username = user_raw[1:]
            chat = await bot.get_chat(f"@{username}")
            return chat.id
        except Exception:
            return None

    return None


@router.message(Command("plus"))
async def plus_handler(message: types.Message) -> None:
    if (
        message.chat.type != "private"
        or not message.from_user
        or message.from_user.id != OWNER_ID
    ):
        return

    chat_id, user_raw = parse_payload(message.text)
    if not chat_id or not user_raw:
        await message.answer(
            "Não deu certo.\n\n"
            "Erro: formato inválido.\n"
            "Use:\n"
            "/plus\n"
            "<chat_id>\n"
            "<user_id ou @username>"
        )
        return

    try:
        user_id = await resolve_user(message.bot, user_raw)
        if not user_id:
            await message.answer("Não consegui identificar o usuário informado.")
            return

        try:
            await message.bot.invite_chat_member(chat_id, user_id)
            await message.answer("Convite enviado com sucesso.")
            return
        except Exception as exc:
            logger.warning(
                "Falha ao convidar membro diretamente; criando link. chat_id=%s user=%s",
                chat_id,
                user_raw,
                exc_info=exc,
            )
            link = await message.bot.create_chat_invite_link(chat_id)
            await message.answer(link.invite_link)
    except Exception as exc:
        logger.exception("Falha no /plus: chat_id=%s user=%s", chat_id, user_raw, exc_info=exc)
        await message.answer("Não deu certo. Verifique se eu tenho permissão no grupo e tente novamente.")
