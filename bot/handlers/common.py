"""
Общие обработчики для помощи и других команд
"""
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from loguru import logger

from bot.utils import get_text
from bot.database import User
from bot.filters import IsRegisteredFilter


router = Router()


@router.message(Command("help"))
@router.message(F.text.in_(["❓ Помощь", "❓ Kömək"]))
async def cmd_help(message: Message, user: User = None):
    """Обработать команду /help"""
    try:
        language = user.language if user else "ru"
        text = get_text("help_text", language)
        
        await message.answer(text)
        
        logger.info(f"Пользователь {message.from_user.id} запросил помощь")
    
    except Exception as e:
        logger.error(f"Ошибка в команде help: {e}")
        await message.answer(get_text("error", "ru"))


@router.message(IsRegisteredFilter())
async def handle_unknown_message(message: Message, user: User):
    """Обработать неизвестные сообщения от зарегистрированных пользователей"""
    try:
        text = get_text("help_text", user.language)
        await message.answer(text)
        
        logger.info(f"Пользователь {user.telegram_id} отправил неизвестное сообщение")
    
    except Exception as e:
        logger.error(f"Ошибка обработки неизвестного сообщения: {e}")