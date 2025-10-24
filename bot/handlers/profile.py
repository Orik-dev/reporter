from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession
from loguru import logger

from bot.states import EditProfileStates
from bot.keyboards import (
    get_edit_profile_keyboard,
    get_language_keyboard,
    get_work_time_keyboard,
    get_cancel_keyboard
)
from bot.utils import get_text
from bot.database import User, UserRepository
from bot.filters import IsRegisteredFilter

router = Router()

@router.message(Command("profile"), IsRegisteredFilter())
@router.message(F.text.in_(["👤 Мой профиль", "👤 Mənim profilim"]), IsRegisteredFilter())
async def cmd_profile(message: Message, user: User, state: FSMContext):
    """Показываем профиль независимо от текущего FSM-состояния"""
    try:
        await state.clear()
        text = get_text("profile_info", user.language,
                        first_name=user.first_name, last_name=user.last_name, work_time=user.work_time)
        await message.answer(text, reply_markup=get_edit_profile_keyboard(user.language))
        logger.info(f"profile shown tg={user.telegram_id}")
    except Exception as e:
        logger.error(f"profile error: {e}")
        await message.answer(get_text("error", user.language))

@router.callback_query(F.data == "edit_first_name")
async def edit_first_name_start(callback: CallbackQuery, state: FSMContext, user: User):
    """Начать редактирование имени"""
    try:
        await callback.answer()
        
        text = get_text("enter_first_name", user.language)
        keyboard = get_cancel_keyboard(user.language)
        
        await callback.message.edit_text(text, reply_markup=keyboard)
        await state.set_state(EditProfileStates.edit_first_name)
        
        logger.info(f"Пользователь {user.telegram_id} начал редактирование имени")
    
    except Exception as e:
        logger.error(f"Ошибка начала редактирования имени: {e}")
        await callback.answer(get_text("error", user.language), show_alert=True)


@router.message(EditProfileStates.edit_first_name, F.text)
async def edit_first_name_process(
    message: Message,
    state: FSMContext,
    user: User,
    session: AsyncSession
):
    """Обработать редактирование имени"""
    try:
        first_name = message.text.strip()
        
        # Валидация имени
        if len(first_name) < 2 or len(first_name) > 50:
            await message.answer(get_text("invalid_input", user.language))
            return
        
        # Обновляем пользователя
        await UserRepository.update(
            session,
            user.telegram_id,
            first_name=first_name
        )
        
        await state.clear()
        
        text = get_text("profile_updated", user.language)
        await message.answer(text)
        
        # Показываем обновленный профиль
        updated_user = await UserRepository.get_by_telegram_id(session, user.telegram_id)
        profile_text = get_text(
            "profile_info",
            updated_user.language,
            first_name=updated_user.first_name,
            last_name=updated_user.last_name,
            work_time=updated_user.work_time
        )
        keyboard = get_edit_profile_keyboard(updated_user.language)
        
        await message.answer(profile_text, reply_markup=keyboard)
        
        logger.info(f"Пользователь {user.telegram_id} обновил имя")
    
    except Exception as e:
        logger.error(f"Ошибка обновления имени: {e}")
        await message.answer(get_text("error", user.language))


@router.callback_query(F.data == "edit_last_name")
async def edit_last_name_start(callback: CallbackQuery, state: FSMContext, user: User):
    """Начать редактирование фамилии"""
    try:
        await callback.answer()
        
        text = get_text("enter_last_name", user.language)
        keyboard = get_cancel_keyboard(user.language)
        
        await callback.message.edit_text(text, reply_markup=keyboard)
        await state.set_state(EditProfileStates.edit_last_name)
        
        logger.info(f"Пользователь {user.telegram_id} начал редактирование фамилии")
    
    except Exception as e:
        logger.error(f"Ошибка начала редактирования фамилии: {e}")
        await callback.answer(get_text("error", user.language), show_alert=True)


@router.message(EditProfileStates.edit_last_name, F.text)
async def edit_last_name_process(
    message: Message,
    state: FSMContext,
    user: User,
    session: AsyncSession
):
    """Обработать редактирование фамилии"""
    try:
        last_name = message.text.strip()
        
        # Валидация фамилии
        if len(last_name) < 2 or len(last_name) > 50:
            await message.answer(get_text("invalid_input", user.language))
            return
        
        # Обновляем пользователя
        await UserRepository.update(
            session,
            user.telegram_id,
            last_name=last_name
        )
        
        await state.clear()
        
        text = get_text("profile_updated", user.language)
        await message.answer(text)
        
        # Показываем обновленный профиль
        updated_user = await UserRepository.get_by_telegram_id(session, user.telegram_id)
        profile_text = get_text(
            "profile_info",
            updated_user.language,
            first_name=updated_user.first_name,
            last_name=updated_user.last_name,
            work_time=updated_user.work_time
        )
        keyboard = get_edit_profile_keyboard(updated_user.language)
        
        await message.answer(profile_text, reply_markup=keyboard)
        
        logger.info(f"Пользователь {user.telegram_id} обновил фамилию")
    
    except Exception as e:
        logger.error(f"Ошибка обновления фамилии: {e}")
        await message.answer(get_text("error", user.language))


@router.callback_query(F.data == "edit_work_time")
async def edit_work_time_start(callback: CallbackQuery, state: FSMContext, user: User):
    """Начать редактирование рабочего времени"""
    try:
        await callback.answer()
        
        text = get_text("select_work_time", user.language)
        keyboard = get_work_time_keyboard(user.language)
        
        await callback.message.edit_text(text, reply_markup=keyboard)
        await state.set_state(EditProfileStates.edit_work_time)
        
        logger.info(f"Пользователь {user.telegram_id} начал редактирование рабочего времени")
    
    except Exception as e:
        logger.error(f"Ошибка начала редактирования рабочего времени: {e}")
        await callback.answer(get_text("error", user.language), show_alert=True)


@router.callback_query(F.data.startswith("work_time_"), EditProfileStates.edit_work_time)
async def edit_work_time_process(
    callback: CallbackQuery,
    state: FSMContext,
    user: User,
    session: AsyncSession
):
    """Обработать редактирование рабочего времени"""
    try:
        work_time_code = callback.data.split("_", 2)[2]
        
        work_time_map = {
            "9-18": "9:00-18:00",
            "10-19": "10:00-19:00"
        }
        work_time = work_time_map.get(work_time_code, "9:00-18:00")
        
        # Обновляем пользователя
        await UserRepository.update(
            session,
            user.telegram_id,
            work_time=work_time
        )
        
        await callback.answer()
        await state.clear()
        
        text = get_text("profile_updated", user.language)
        await callback.message.edit_text(text)
        
        # Показываем обновленный профиль
        updated_user = await UserRepository.get_by_telegram_id(session, user.telegram_id)
        profile_text = get_text(
            "profile_info",
            updated_user.language,
            first_name=updated_user.first_name,
            last_name=updated_user.last_name,
            work_time=updated_user.work_time
        )
        keyboard = get_edit_profile_keyboard(updated_user.language)
        
        await callback.message.answer(profile_text, reply_markup=keyboard)
        
        logger.info(f"Пользователь {user.telegram_id} обновил рабочее время на {work_time}")
    
    except Exception as e:
        logger.error(f"Ошибка обновления рабочего времени: {e}")
        await callback.answer(get_text("error", user.language), show_alert=True)


@router.callback_query(F.data == "edit_language")
async def edit_language_start(callback: CallbackQuery, state: FSMContext, user: User):
    """Начать редактирование языка"""
    try:
        await callback.answer()
        
        text = get_text("welcome", user.language)
        keyboard = get_language_keyboard()
        
        await callback.message.edit_text(text, reply_markup=keyboard)
        await state.set_state(EditProfileStates.edit_language)
        
        logger.info(f"Пользователь {user.telegram_id} начал редактирование языка")
    
    except Exception as e:
        logger.error(f"Ошибка начала редактирования языка: {e}")
        await callback.answer(get_text("error", user.language), show_alert=True)


@router.callback_query(F.data.startswith("lang_"), EditProfileStates.edit_language)
async def edit_language_process(
    callback: CallbackQuery,
    state: FSMContext,
    user: User,
    session: AsyncSession
):
    """Обработать редактирование языка"""
    try:
        language = callback.data.split("_")[1]
        
        # Обновляем пользователя
        await UserRepository.update(
            session,
            user.telegram_id,
            language=language
        )
        
        await callback.answer()
        await state.clear()
        
        text = get_text("profile_updated", language)
        await callback.message.edit_text(text)
        
        # Показываем обновленный профиль
        updated_user = await UserRepository.get_by_telegram_id(session, user.telegram_id)
        profile_text = get_text(
            "profile_info",
            updated_user.language,
            first_name=updated_user.first_name,
            last_name=updated_user.last_name,
            work_time=updated_user.work_time
        )
        keyboard = get_edit_profile_keyboard(updated_user.language)
        
        await callback.message.answer(profile_text, reply_markup=keyboard)
        
        logger.info(f"Пользователь {user.telegram_id} обновил язык на {language}")
    
    except Exception as e:
        logger.error(f"Ошибка обновления языка: {e}")
        await callback.answer(get_text("error", user.language), show_alert=True)


@router.callback_query(F.data == "back_to_menu")
async def back_to_menu(callback: CallbackQuery, state: FSMContext, user: User):
    """Обработать кнопку возврата в меню"""
    try:
        await state.clear()
        await callback.answer()
        
        text = get_text("help_text", user.language)
        await callback.message.edit_text(text)
        
        logger.info(f"Пользователь {user.telegram_id} вернулся в меню")
    
    except Exception as e:
        logger.error(f"Ошибка возврата в меню: {e}")

        await callback.answer(get_text("error", user.language), show_alert=True)

