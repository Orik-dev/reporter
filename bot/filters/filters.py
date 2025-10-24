"""
Кастомные фильтры для aiogram 3.22
"""
from typing import Any
from aiogram.filters import BaseFilter
from aiogram.types import TelegramObject


class IsRegisteredFilter(BaseFilter):
    """Пользователь зарегистрирован"""
    async def __call__(self, event: TelegramObject, **data: Any) -> bool:
        return bool(data.get("is_registered", False))


class IsNotRegisteredFilter(BaseFilter):
    """Пользователь НЕ зарегистрирован"""
    async def __call__(self, event: TelegramObject, **data: Any) -> bool:
        return not bool(data.get("is_registered", False))


class IsAdminFilter(BaseFilter):
    """Пользователь — админ"""
    async def __call__(self, event: TelegramObject, **data: Any) -> bool:
        return bool(data.get("is_admin", False))
