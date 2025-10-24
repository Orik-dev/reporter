"""
Кастомные фильтры для aiogram 3.22.0
"""
from aiogram.filters import BaseFilter


class IsRegisteredFilter(BaseFilter):
    async def __call__(self, event, is_registered=False, **kwargs):
        return is_registered


class IsNotRegisteredFilter(BaseFilter):
    async def __call__(self, event, is_registered=False, **kwargs):
        return not is_registered


class IsAdminFilter(BaseFilter):
    async def __call__(self, event, is_admin=False, **kwargs):
        return is_admin


class IsNotAdminFilter(BaseFilter):
    """Пользователь НЕ админ"""
    async def __call__(self, event, is_admin=False, **kwargs):
        return not is_admin