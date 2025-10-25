# """
# Отчеты - ИСПРАВЛЕННАЯ ВЕРСИЯ
# """
# from aiogram import Router, F
# from aiogram.filters import Command
# from aiogram.types import Message, CallbackQuery
# from aiogram.fsm.context import FSMContext
# from sqlalchemy.ext.asyncio import AsyncSession
# from datetime import date, datetime
# from loguru import logger

# from bot.states import ReportStates
# from bot.keyboards import get_report_type_keyboard
# from bot.utils import get_text
# from bot.database import User, DailyReportRepository
# from bot.filters import IsRegisteredFilter

# router = Router()


# @router.message(Command("report"), IsRegisteredFilter())
# @router.message(F.text.in_(["📊 Отправить отчет", "📊 Hesabat göndər"]), IsRegisteredFilter())
# async def cmd_report(message: Message, user: User, session: AsyncSession, state: FSMContext):
#     """Начать отправку отчета"""
#     try:
#         await state.clear()
#         today = date.today()
#         existing = await DailyReportRepository.get_by_date(session, user.telegram_id, today)
#         if existing:
#             await message.answer(get_text("report_already_submitted", user.language))
#             return
#         await message.answer(get_text("report_type_select", user.language),
#                              reply_markup=get_report_type_keyboard(user.language))
#         await state.set_state(ReportStates.waiting_for_report)
#         logger.info(f"report started tg={user.telegram_id}")
#     except Exception as e:
#         logger.error(f"report start error: {e}")
#         await message.answer(get_text("error", user.language))


# @router.callback_query(F.data == "report_has_tasks", ReportStates.waiting_for_report)
# async def report_has_tasks(callback: CallbackQuery, state: FSMContext, user: User):
#     """Пользователь выбрал что есть задачи"""
#     try:
#         await callback.answer()
#         text = get_text("enter_report_text", user.language)
#         await callback.message.edit_text(text)
#         await state.update_data(has_tasks=True)
#         logger.info(f"Пользователь {user.telegram_id} выбрал 'есть задачи'")
#     except Exception as e:
#         logger.error(f"Ошибка в report_has_tasks: {e}")
#         await callback.answer(get_text("error", user.language), show_alert=True)


# @router.callback_query(F.data == "report_no_tasks", ReportStates.waiting_for_report)
# async def report_no_tasks(
#     callback: CallbackQuery,
#     state: FSMContext,
#     user: User,
#     session: AsyncSession
# ):
#     """Пользователь выбрал что нет задач"""
#     try:
#         today = datetime.now()
        
#         await DailyReportRepository.create(
#             session=session,
#             user_id=user.id,
#             telegram_id=user.telegram_id,
#             report_date=today,
#             report_text=None,
#             has_tasks=False
#         )
        
#         await callback.answer()
#         await state.clear()
        
#         text = get_text("report_no_tasks", user.language)
#         await callback.message.edit_text(text)
        
#         logger.info(f"Пользователь {user.telegram_id} сообщил об отсутствии задач")
    
#     except Exception as e:
#         logger.error(f"Ошибка в report_no_tasks: {e}")
#         await callback.answer(get_text("error", user.language), show_alert=True)


# @router.message(ReportStates.waiting_for_report, F.text)
# async def receive_report_text(
#     message: Message,
#     state: FSMContext,
#     user: User,
#     session: AsyncSession
# ):
#     """Получить текст отчета"""
#     try:
#         data = await state.get_data()
#         has_tasks = data.get('has_tasks', True)
        
#         if not has_tasks:
#             await message.answer(get_text("invalid_input", user.language))
#             return
        
#         report_text = message.text.strip()
        
#         # ✅ ИСПРАВЛЕНО: Улучшенная валидация отчета
#         # Проверка 1: Не пустой
#         if not report_text:
#             await message.answer(get_text("report_empty", user.language))
#             return
        
#         # Проверка 2: Минимум 10 символов
#         if len(report_text) < 10:
#             await message.answer(get_text("report_too_short", user.language))
#             return
        
#         # Проверка 3: Не только пробелы и переносы строк
#         if not report_text.replace('\n', '').replace(' ', ''):
#             await message.answer(get_text("report_empty", user.language))
#             return
        
#         # Сохраняем отчет
#         today = datetime.now()
        
#         await DailyReportRepository.create(
#             session=session,
#             user_id=user.id,
#             telegram_id=user.telegram_id,
#             report_date=today,
#             report_text=report_text,
#             has_tasks=True
#         )
        
#         await state.clear()
        
#         text = get_text("report_submitted", user.language)
#         await message.answer(text)
        
#         logger.info(f"Пользователь {user.telegram_id} отправил ежедневный отчет")
    
#     except Exception as e:
#         logger.error(f"Ошибка получения текста отчета: {e}")
#         await message.answer(get_text("error", user.language))


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

from bot.states import ReportStates
from bot.keyboards import get_report_type_keyboard, get_cancel_report_keyboard
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
        today = date.today()
        existing = await DailyReportRepository.get_by_date(session, user.telegram_id, today)
        if existing:
            await message.answer(get_text("report_already_submitted", user.language))
            return
        await message.answer(get_text("report_type_select", user.language),
                             reply_markup=get_report_type_keyboard(user.language))
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
        # ✅ НОВОЕ: Добавлена кнопка отмены
        keyboard = get_cancel_report_keyboard(user.language)
        await callback.message.edit_text(text, reply_markup=keyboard)
        await state.update_data(has_tasks=True)
        logger.info(f"Пользователь {user.telegram_id} выбрал 'есть задачи'")
    except Exception as e:
        logger.error(f"Ошибка в report_has_tasks: {e}")
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


# ✅ НОВОЕ: Обработчик кнопки "Отменить отправку отчета"
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