"""
Middleware - ИСПРАВЛЕННАЯ ВЕРСИЯ
"""
from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message, CallbackQuery
from loguru import logger

from bot.database import db_manager, UserRepository
from config.settings import settings as app_settings


class LoggingMiddleware(BaseMiddleware):
    """Логирование входящих сообщений"""
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
    """Создание сессии БД для каждого update"""
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        async with db_manager.session() as session:
            data["session"] = session
            try:
                return await handler(event, data)
            finally:
                if session.in_transaction():
                    await session.rollback()


class UserCheckMiddleware(BaseMiddleware):
    """Проверка регистрации пользователя"""
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
                logger.debug(f"[UserCheck] найден user {user.telegram_id} ({user.first_name}), is_admin={user.is_admin}")
            else:
                logger.debug(f"[UserCheck] пользователь {tg_user.id} не найден в БД")
        except Exception as e:
            logger.error(f"UserCheck error: {e}")
            data["user"] = None
            data["is_registered"] = False

        return await handler(event, data)


class AdminCheckMiddleware(BaseMiddleware):
    """Проверка прав администратора"""
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

        # ✅ ИСПРАВЛЕНО: Детальное логирование ADMIN_IDS
        try:
            logger.debug(f"[AdminCheck] raw ADMIN_IDS from settings: '{app_settings.admin_ids}'")
            admin_list = app_settings.admin_ids_list or []
            logger.debug(f"[AdminCheck] parsed admin_ids_list: {admin_list}")
        except Exception as e:
            logger.error(f"[AdminCheck] ОШИБКА получения admin_ids: {e}")
            admin_list = []

        env_admin = tg_user.id in admin_list
        db_admin = bool(getattr(user, "is_admin", False))
        is_admin = env_admin or db_admin

        data["is_admin"] = is_admin
        
        # ✅ ИСПРАВЛЕНО: Подробное логирование
        logger.info(
            f"[AdminCheck] tg_id={tg_user.id} | "
            f"is_admin={is_admin} | "
            f"env_admin={env_admin} | "
            f"db_admin={db_admin} | "
            f"ADMIN_IDS={admin_list}"
        )

        return await handler(event, data)