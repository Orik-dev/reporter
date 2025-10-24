"""
Middleware для бота
"""
from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message, CallbackQuery
from loguru import logger

from bot.database import db_manager, UserRepository
from config.settings import settings as app_settings


class LoggingMiddleware(BaseMiddleware):
    """Логирует входящие сообщения и callback-и"""
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        if isinstance(event, Message):
            logger.info(f"Сообщение от {event.from_user.id} ({event.from_user.username}): {event.text or ''}")
        elif isinstance(event, CallbackQuery):
            logger.info(f"Callback от {event.from_user.id} ({event.from_user.username}): {event.data}")
        return await handler(event, data)


class DatabaseMiddleware(BaseMiddleware):
    """Создаёт и передаёт session в data для всех апдейтов"""
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        # создаём отдельную сессию на каждый update
        async with db_manager.session() as session:
            data["session"] = session
            try:
                return await handler(event, data)
            finally:
                # если по какой-то причине транзакция не закрыта
                if session.in_transaction():
                    await session.rollback()


class UserCheckMiddleware(BaseMiddleware):
    """Проверяет, зарегистрирован ли пользователь. Кладёт в data: user, is_registered"""
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        tg_user = None
        if isinstance(event, Message):
            tg_user = event.from_user
        elif isinstance(event, CallbackQuery):
            tg_user = event.from_user

        if not tg_user:
            return await handler(event, data)

        session = data.get("session")
        if not session:
            return await handler(event, data)

        try:
            user = await UserRepository.get_by_telegram_id(session, tg_user.id)
            data["user"] = user
            data["is_registered"] = user is not None

            if user:
                logger.info(f"[UserCheck] найден user {user.telegram_id} ({user.first_name}), is_admin={user.is_admin}")
            else:
                logger.info(f"[UserCheck] пользователь {tg_user.id} не найден в БД")
        except Exception as e:
            logger.error(f"UserCheck error: {e}")
            data["user"] = None
            data["is_registered"] = False

        return await handler(event, data)


class AdminCheckMiddleware(BaseMiddleware):
    """Кладёт в data: is_admin (по .env ИЛИ по флагу в БД)"""
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        tg_user = event.from_user if isinstance(event, (Message, CallbackQuery)) else None
        if not tg_user:
            return await handler(event, data)

        user = data.get("user")

        try:
            admin_list = app_settings.admin_ids_list or []
        except Exception as e:
            logger.error(f"AdminCheck: settings недоступны: {e}")
            admin_list = []

        env_admin = tg_user.id in admin_list
        db_admin = bool(getattr(user, "is_admin", False))
        is_admin = env_admin or db_admin

        data["is_admin"] = is_admin
        logger.info(
            f"[AdminCheck] is_admin={is_admin} (env={env_admin}, db={db_admin}) "
            f"for tg_id={tg_user.id}; ADMIN_IDS={admin_list}"
        )

        return await handler(event, data)