"""
Отчеты - ФИНАЛЬНАЯ ВЕРСИЯ
"""
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import date, datetime
from loguru import logger
import pytz

from config.settings import settings
from bot.states import ReportStates
from bot.keyboards import (
    get_report_type_keyboard, 
    get_cancel_and_examples_keyboard,
    get_examples_keyboard
)
from bot.utils import get_text
from bot.database import User, DailyReportRepository
from bot.filters import IsRegisteredFilter

router = Router()


@router.message(Command("report"), IsRegisteredFilter())
@router.message(F.text.in_(["📊 Отправить отчет", "📊 Hesabat göndər"]), IsRegisteredFilter())
async def cmd_report(message: Message, user: User, session: AsyncSession, state: FSMContext):
    """Начать отправку отчета"""
    try:
        await state.clear()
        
        # ✅ НОВОЕ: Проверка времени
        baku_tz = pytz.timezone(settings.timezone)
        now_baku = datetime.now(baku_tz)
        current_hour = now_baku.hour
        
        # Определяем конец рабочего дня
        if user.work_time == "9:00-18:00":
            end_hour = 18
        else:  # "10:00-19:00"
            end_hour = 19
        
        # Если еще не конец рабочего дня
        if current_hour < end_hour:
            text = get_text("report_too_early", user.language, end_time=f"{end_hour}:00")
            await message.answer(text)
            logger.info(f"report blocked (too early) tg={user.telegram_id}, hour={current_hour}, end={end_hour}")
            return
        
        today = date.today()
        existing = await DailyReportRepository.get_by_date(session, user.telegram_id, today)
        if existing:
            await message.answer(get_text("report_already_submitted", user.language))
            return
            
        await message.answer(
            get_text("report_type_select", user.language),
            reply_markup=get_report_type_keyboard(user.language)
        )
        await state.set_state(ReportStates.waiting_for_report)
        logger.info(f"report started tg={user.telegram_id}")
    except Exception as e:
        logger.error(f"report start error: {e}")
        await message.answer(get_text("error", user.language))


@router.callback_query(F.data == "report_has_tasks", ReportStates.waiting_for_report)
async def report_has_tasks(callback: CallbackQuery, state: FSMContext, user: User):
    """Пользователь выбрал что есть задачи"""
    try:
        await callback.answer()
        text = get_text("enter_report_text", user.language)
        # ✅ ОБНОВЛЕНО: Кнопки отмены и примеров
        keyboard = get_cancel_and_examples_keyboard(user.language)
        await callback.message.edit_text(text, reply_markup=keyboard)
        await state.update_data(has_tasks=True)
        logger.info(f"Пользователь {user.telegram_id} выбрал 'есть задачи'")
    except Exception as e:
        logger.error(f"Ошибка в report_has_tasks: {e}")
        await callback.answer(get_text("error", user.language), show_alert=True)


@router.callback_query(F.data == "show_examples", ReportStates.waiting_for_report)
async def show_examples(callback: CallbackQuery, state: FSMContext, user: User):
    """Показать примеры отчетов"""
    try:
        await callback.answer()
        text = get_text("examples_header", user.language)
        keyboard = get_examples_keyboard(user.language)
        await callback.message.edit_text(text, reply_markup=keyboard)
        logger.info(f"Пользователь {user.telegram_id} открыл примеры")
    except Exception as e:
        logger.error(f"Ошибка show_examples: {e}")
        await callback.answer(get_text("error", user.language), show_alert=True)


@router.callback_query(F.data.startswith("example_"), ReportStates.waiting_for_report)
async def show_example_text(callback: CallbackQuery, state: FSMContext, user: User):
    """Показать конкретный пример"""
    try:
        example_type = callback.data.split("_", 1)[1]
        text = get_text(f"example_{example_type}", user.language)
        keyboard = get_examples_keyboard(user.language)
        await callback.message.edit_text(text, reply_markup=keyboard)
        await callback.answer()
        logger.info(f"Пользователь {user.telegram_id} посмотрел пример {example_type}")
    except Exception as e:
        logger.error(f"Ошибка show_example_text: {e}")
        await callback.answer(get_text("error", user.language), show_alert=True)


@router.callback_query(F.data == "back_to_report", ReportStates.waiting_for_report)
async def back_to_report(callback: CallbackQuery, state: FSMContext, user: User):
    """Вернуться к вводу отчета"""
    try:
        await callback.answer()
        text = get_text("enter_report_text", user.language)
        keyboard = get_cancel_and_examples_keyboard(user.language)
        await callback.message.edit_text(text, reply_markup=keyboard)
        logger.info(f"Пользователь {user.telegram_id} вернулся к вводу отчета")
    except Exception as e:
        logger.error(f"Ошибка back_to_report: {e}")
        await callback.answer(get_text("error", user.language), show_alert=True)


@router.callback_query(F.data == "report_no_tasks", ReportStates.waiting_for_report)
async def report_no_tasks(
    callback: CallbackQuery,
    state: FSMContext,
    user: User,
    session: AsyncSession
):
    """Пользователь выбрал что нет задач"""
    try:
        today = datetime.now()
        
        await DailyReportRepository.create(
            session=session,
            user_id=user.id,
            telegram_id=user.telegram_id,
            report_date=today,
            report_text=None,
            has_tasks=False
        )
        
        await callback.answer()
        await state.clear()
        
        text = get_text("report_no_tasks", user.language)
        await callback.message.edit_text(text)
        
        logger.info(f"Пользователь {user.telegram_id} сообщил об отсутствии задач")
    
    except Exception as e:
        logger.error(f"Ошибка в report_no_tasks: {e}")
        await callback.answer(get_text("error", user.language), show_alert=True)


@router.callback_query(F.data == "cancel_report", ReportStates.waiting_for_report)
async def cancel_report(callback: CallbackQuery, state: FSMContext, user: User):
    """Отменить отправку отчета"""
    try:
        await state.clear()
        await callback.answer("Отменено / Ləğv edildi")
        
        text = get_text("report_cancelled", user.language)
        await callback.message.edit_text(text)
        
        logger.info(f"Пользователь {user.telegram_id} отменил отправку отчета")
    except Exception as e:
        logger.error(f"Ошибка отмены отчета: {e}")
        await callback.answer(get_text("error", user.language), show_alert=True)


@router.message(ReportStates.waiting_for_report, F.text)
async def receive_report_text(
    message: Message,
    state: FSMContext,
    user: User,
    session: AsyncSession
):
    """Получить текст отчета"""
    try:
        data = await state.get_data()
        has_tasks = data.get('has_tasks', True)
        
        if not has_tasks:
            await message.answer(get_text("invalid_input", user.language))
            return
        
        report_text = message.text.strip()
        
        # Валидация
        if not report_text:
            await message.answer(get_text("report_empty", user.language))
            return
        
        if len(report_text) < 10:
            await message.answer(get_text("report_too_short", user.language))
            return
        
        if not report_text.replace('\n', '').replace(' ', ''):
            await message.answer(get_text("report_empty", user.language))
            return
        
        # Сохраняем отчет
        today = datetime.now()
        
        await DailyReportRepository.create(
            session=session,
            user_id=user.id,
            telegram_id=user.telegram_id,
            report_date=today,
            report_text=report_text,
            has_tasks=True
        )
        
        await state.clear()
        
        text = get_text("report_submitted", user.language)
        await message.answer(text)
        
        logger.info(f"Пользователь {user.telegram_id} отправил ежедневный отчет")
    
    except Exception as e:
        logger.error(f"Ошибка получения текста отчета: {e}")
        await message.answer(get_text("error", user.language))