"""
/start и регистрация
"""
from aiogram import Router, F
from aiogram.filters import CommandStart, StateFilter
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession
from loguru import logger

from config.settings import settings
from bot.states import RegistrationStates
from bot.keyboards import (
    get_language_keyboard,
    get_work_time_keyboard,
    get_confirmation_keyboard,
    get_main_menu_keyboard,
)
from bot.utils import get_text
from bot.database import User, UserRepository
from bot.filters import IsNotRegisteredFilter, IsRegisteredFilter

router = Router()

# -------- /start --------

@router.message(CommandStart(), IsRegisteredFilter())
async def cmd_start_registered(message: Message, user: User, state: FSMContext):
    """Зарегистрированным показываем меню, сбрасываем любые состояния"""
    try:
        await state.clear()
        await message.answer(
            get_text("help_text", user.language),
            reply_markup=get_main_menu_keyboard(user.language, user.is_admin),
        )
        logger.info(f"/start (registered) tg_id={user.telegram_id}")
    except Exception as e:
        logger.error(f"start registered error: {e}")
        await message.answer(get_text("error", user.language))


@router.message(CommandStart(), IsNotRegisteredFilter())
async def cmd_start_not_registered(message: Message, state: FSMContext):
    """Незарегистрированным — выбор языка и запуск регистрации"""
    try:
        await state.clear()
        await message.answer(get_text("welcome", "ru"), reply_markup=get_language_keyboard())
        await state.set_state(RegistrationStates.language)
        logger.info(f"/start -> registration tg_id={message.from_user.id}")
    except Exception as e:
        logger.error(f"start not registered error: {e}")
        await message.answer(get_text("error", "ru"))

# -------- Регистрация --------

@router.callback_query(F.data.startswith("lang_"), RegistrationStates.language)
async def select_language(callback: CallbackQuery, state: FSMContext):
    try:
        lang = callback.data.split("_", 1)[1]
        await state.update_data(language=lang)
        await callback.message.edit_text(get_text("enter_first_name", lang))
        await state.set_state(RegistrationStates.first_name)
        await callback.answer()
        logger.info(f"lang selected={lang} tg={callback.from_user.id}")
    except Exception as e:
        logger.error(f"select_language error: {e}")
        await callback.answer(get_text("error", "ru"), show_alert=True)


def _bad_name(s: str) -> bool:
    if not s:
        return True
    s = s.strip()
    if len(s) < 2 or len(s) > 50:
        return True
    if s.startswith("/"):
        return True
    banned = {
        "👤 Мой профиль", "📊 Отправить отчет", "❓ Помощь", "⚙️ Админ-панель",
        "👤 Mənim profilim", "📊 Hesabat göndər", "❓ Kömək", "⚙️ Admin panel",
    }
    return s in banned


@router.message(RegistrationStates.first_name, F.text)
async def enter_first_name(message: Message, state: FSMContext):
    try:
        data = await state.get_data()
        lang = data.get("language", "ru")
        name = message.text.strip()
        if _bad_name(name):
            await message.answer(get_text("invalid_input", lang))
            return
        await state.update_data(first_name=name)
        await message.answer(get_text("enter_last_name", lang))
        await state.set_state(RegistrationStates.last_name)
        logger.info(f"first_name ok tg={message.from_user.id}")
    except Exception as e:
        logger.error(f"enter_first_name error: {e}")
        await message.answer(get_text("error", "ru"))


@router.message(RegistrationStates.last_name, F.text)
async def enter_last_name(message: Message, state: FSMContext):
    try:
        data = await state.get_data()
        lang = data.get("language", "ru")
        last = message.text.strip()
        if _bad_name(last):
            await message.answer(get_text("invalid_input", lang))
            return
        await state.update_data(last_name=last)
        await message.answer(get_text("select_work_time", lang), reply_markup=get_work_time_keyboard(lang))
        await state.set_state(RegistrationStates.work_time)
        logger.info(f"last_name ok tg={message.from_user.id}")
    except Exception as e:
        logger.error(f"enter_last_name error: {e}")
        await message.answer(get_text("error", "ru"))


@router.callback_query(F.data.startswith("work_time_"), RegistrationStates.work_time)
async def select_work_time(callback: CallbackQuery, state: FSMContext):
    try:
        code = callback.data.split("_", 2)[2]
        work_time = {"9-18": "9:00-18:00", "10-19": "10:00-19:00"}.get(code, "9:00-18:00")
        await state.update_data(work_time=work_time)
        data = await state.get_data()
        lang = data["language"]
        await callback.message.edit_text(
            get_text("confirm_registration", lang,
                     first_name=data["first_name"], last_name=data["last_name"], work_time=work_time),
            reply_markup=get_confirmation_keyboard(lang)
        )
        await state.set_state(RegistrationStates.confirmation)
        await callback.answer()
        logger.info(f"work_time={work_time} tg={callback.from_user.id}")
    except Exception as e:
        logger.error(f"select_work_time error: {e}")
        await callback.answer(get_text("error", "ru"), show_alert=True)


@router.callback_query(F.data == "confirm_yes", RegistrationStates.confirmation)
async def confirm_registration(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
    try:
        data = await state.get_data()
        lang = data["language"]
        # флаг админа из .env
        is_admin = callback.from_user.id in settings.admin_ids_list

        await UserRepository.create(
            session=session,
            telegram_id=callback.from_user.id,
            first_name=data["first_name"],
            last_name=data["last_name"],
            language=lang,
            work_time=data["work_time"],
            is_admin=is_admin
        )

        await state.clear()
        await callback.message.edit_text(get_text("registration_success", lang))
        await callback.message.answer(
            get_text("help_text", lang),
            reply_markup=get_main_menu_keyboard(lang, is_admin)
        )
        await callback.answer()
        logger.info(f"registration done tg={callback.from_user.id} is_admin_env={is_admin}")
    except Exception as e:
        logger.error(f"confirm_registration error: {e}")
        await callback.answer(get_text("error", "ru"), show_alert=True)


@router.callback_query(F.data == "confirm_edit", RegistrationStates.confirmation)
async def confirm_edit(callback: CallbackQuery, state: FSMContext):
    """Вернуться к имени (исправить данные)"""
    try:
        data = await state.get_data()
        lang = data.get("language", "ru")
        await callback.message.edit_text(get_text("enter_first_name", lang))
        await state.set_state(RegistrationStates.first_name)
        await callback.answer()
    except Exception as e:
        logger.error(f"confirm_edit error: {e}")
        await callback.answer(get_text("error", "ru"), show_alert=True)
