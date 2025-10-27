"""
Обработчики для админ-панели - С ФУНКЦИЕЙ УДАЛЕНИЯ ПОЛЬЗОВАТЕЛЕЙ
"""
from datetime import date, datetime, timedelta
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, BufferedInputFile
from sqlalchemy.ext.asyncio import AsyncSession
from loguru import logger

from bot.keyboards import get_admin_keyboard, get_user_list_keyboard, get_delete_confirmation_keyboard
from bot.utils import get_text, format_answer
from bot.database import User, UserRepository, DailyReportRepository
from bot.filters import IsAdminFilter, IsNotAdminFilter
from bot.services import deepseek_service, document_service
from bot.services.scheduler_service import SchedulerService

router = Router()

# Хранилище для отслеживания генерации отчетов
generating_reports = {}


@router.message(Command("admin"), IsAdminFilter())
@router.message(F.text.in_(["⚙️ Админ-панель", "⚙️ Admin panel"]), IsAdminFilter())
async def cmd_admin(message: Message, user: User):
    """Админ-панель"""
    try:
        language = user.language if user else "ru"
        text = get_text("admin_panel", language)
        keyboard = get_admin_keyboard(language)
        
        await message.answer(text, reply_markup=keyboard)
        
        logger.info(f"✅ Администратор {message.from_user.id} открыл админ-панель")
    
    except Exception as e:
        logger.error(f"Ошибка в команде admin: {e}")
        language = user.language if user else "ru"
        await message.answer(get_text("error", language))


@router.message(Command("admin"), IsNotAdminFilter())
@router.message(F.text.in_(["⚙️ Админ-панель", "⚙️ Admin panel"]), IsNotAdminFilter())
async def cmd_admin_not_authorized(message: Message, user: User):
    """Попытка доступа без прав"""
    try:
        language = user.language if user else "ru"
        text = get_text("not_authorized", language)
        await message.answer(text)
        
        logger.warning(f"⚠️ Пользователь {message.from_user.id} попытался войти в админ-панель без прав")
    
    except Exception as e:
        logger.error(f"Ошибка в admin not authorized: {e}")


@router.callback_query(F.data == "admin_stats", IsAdminFilter())
async def admin_stats(callback: CallbackQuery, user: User, session: AsyncSession):
    """Показать статистику"""
    try:
        language = user.language if user else "ru"
        
        all_users = await UserRepository.get_all_active(session)
        total_users = len(all_users)
        
        today = date.today()
        start_date = datetime.combine(today, datetime.min.time())
        end_date = datetime.combine(today, datetime.max.time())
        today_reports = await DailyReportRepository.get_reports_by_date_range(
            session,
            start_date,
            end_date
        )
        
        week_start = today - timedelta(days=today.weekday())
        week_start_date = datetime.combine(week_start, datetime.min.time())
        week_reports = await DailyReportRepository.get_reports_by_date_range(
            session,
            week_start_date,
            end_date
        )
        
        text = get_text(
            "stats",
            language,
            total_users=total_users,
            active_users=total_users,
            today_reports=len(today_reports),
            week_reports=len(week_reports)
        )
        
        await callback.message.edit_text(text)
        await callback.answer()
        
        logger.info(f"Администратор {callback.from_user.id} просмотрел статистику")
    
    except Exception as e:
        logger.error(f"Ошибка показа статистики: {e}")
        language = user.language if user else "ru"
        await callback.answer(get_text("error", language), show_alert=True)


@router.callback_query(F.data == "admin_users", IsAdminFilter())
async def admin_users(callback: CallbackQuery, user: User, session: AsyncSession):
    """Показать список пользователей с кнопками удаления"""
    try:
        language = user.language if user else "ru"
        
        users = await UserRepository.get_all_active(session)
        
        users_text = ""
        for u in users:
            admin_badge = " 👑" if u.is_admin else ""
            users_text += f"• {u.first_name} {u.last_name} ({u.work_time}){admin_badge}\n"
        
        text = get_text(
            "user_list",
            language,
            count=len(users),
            users=users_text
        )
        
        keyboard = get_user_list_keyboard(users, language, callback.from_user.id)
        
        await callback.message.edit_text(text, reply_markup=keyboard)
        await callback.answer()
        
        logger.info(f"Администратор {callback.from_user.id} просмотрел список пользователей")
    
    except Exception as e:
        logger.error(f"Ошибка показа пользователей: {e}")
        language = user.language if user else "ru"
        await callback.answer(get_text("error", language), show_alert=True)


@router.callback_query(F.data.startswith("delete_user_"), IsAdminFilter())
async def delete_user_confirm(callback: CallbackQuery, user: User, session: AsyncSession):
    """
    ✅ ИСПРАВЛЕНО: Подтверждение удаления пользователя
    """
    try:
        # ✅ ИСПРАВЛЕНО: Определяем язык сразу
        language = user.language if user else "ru"
        
        telegram_id = int(callback.data.split("_")[2])
        
        # Проверка: нельзя удалить самого себя
        if telegram_id == callback.from_user.id:
            await callback.answer(
                get_text("cannot_delete_self", language),
                show_alert=True
            )
            return
        
        # Получаем информацию о пользователе
        target_user = await UserRepository.get_by_telegram_id(session, telegram_id)
        if not target_user:
            await callback.answer(
                get_text("user_not_found", language),
                show_alert=True
            )
            return
        
        # Проверка: нельзя удалить другого админа
        if target_user.is_admin:
            await callback.answer(
                get_text("cannot_delete_admin", language),
                show_alert=True
            )
            return
        
        # Показываем подтверждение
        text = get_text(
            "delete_user_confirm",
            language,
            first_name=target_user.first_name,
            last_name=target_user.last_name
        )
        
        keyboard = get_delete_confirmation_keyboard(telegram_id, language)
        
        await callback.message.edit_text(text, reply_markup=keyboard)
        await callback.answer()
        
        logger.info(f"Админ {callback.from_user.id} запросил удаление пользователя {telegram_id}")
    
    except Exception as e:
        logger.error(f"Ошибка при подтверждении удаления: {e}")
        language = user.language if user else "ru"
        await callback.answer(get_text("error", language), show_alert=True)


@router.callback_query(F.data.startswith("confirm_delete_"), IsAdminFilter())
async def delete_user_execute(callback: CallbackQuery, user: User, session: AsyncSession):
    """
    ✅ ИСПРАВЛЕНО: Выполнить удаление пользователя
    """
    try:
        # ✅ ИСПРАВЛЕНО: Определяем язык сразу
        language = user.language if user else "ru"
        
        telegram_id = int(callback.data.split("_")[2])
        
        # Получаем информацию о пользователе до удаления
        target_user = await UserRepository.get_by_telegram_id(session, telegram_id)
        if not target_user:
            await callback.answer(
                get_text("user_not_found", language),
                show_alert=True
            )
            return
        
        user_name = f"{target_user.first_name} {target_user.last_name}"
        
        # Удаляем пользователя
        success = await UserRepository.delete_user(session, telegram_id)
        
        if success:
            text = get_text(
                "user_deleted",
                language,
                first_name=target_user.first_name,
                last_name=target_user.last_name
            )
            
            await callback.message.edit_text(text)
            await callback.answer("✅ Удалено" if language == "ru" else "✅ Silindi")
            
            logger.info(f"Админ {callback.from_user.id} удалил пользователя {telegram_id} ({user_name})")
        else:
            await callback.answer(
                get_text("user_not_found", language),
                show_alert=True
            )
    
    except Exception as e:
        logger.error(f"Ошибка при удалении пользователя: {e}")
        language = user.language if user else "ru"
        await callback.answer(get_text("error", language), show_alert=True)


@router.callback_query(F.data.startswith("cancel_delete_"), IsAdminFilter())
async def delete_user_cancel(callback: CallbackQuery, user: User, session: AsyncSession):
    """
    ✅ ИСПРАВЛЕНО: Отменить удаление пользователя
    """
    try:
        # ✅ ИСПРАВЛЕНО: Определяем язык сразу
        language = user.language if user else "ru"
        
        # Возвращаемся к списку пользователей
        users = await UserRepository.get_all_active(session)
        
        users_text = ""
        for u in users:
            admin_badge = " 👑" if u.is_admin else ""
            users_text += f"• {u.first_name} {u.last_name} ({u.work_time}){admin_badge}\n"
        
        text = get_text(
            "user_list",
            language,
            count=len(users),
            users=users_text
        )
        
        keyboard = get_user_list_keyboard(users, language, callback.from_user.id)
        
        await callback.message.edit_text(text, reply_markup=keyboard)
        await callback.answer("❌ Отменено" if language == "ru" else "❌ Ləğv edildi")
        
        logger.info(f"Админ {callback.from_user.id} отменил удаление пользователя")
    
    except Exception as e:
        logger.error(f"Ошибка при отмене удаления: {e}")
        language = user.language if user else "ru"
        await callback.answer(get_text("error", language), show_alert=True)


@router.callback_query(F.data == "admin_panel_back", IsAdminFilter())
async def admin_panel_back(callback: CallbackQuery, user: User):
    """Возврат в админ-панель"""
    try:
        language = user.language if user else "ru"
        text = get_text("admin_panel", language)
        keyboard = get_admin_keyboard(language)
        
        await callback.message.edit_text(text, reply_markup=keyboard)
        await callback.answer()
        
        logger.info(f"Админ {callback.from_user.id} вернулся в главное меню админ-панели")
        
    except Exception as e:
        logger.error(f"Ошибка возврата в админ-панель: {e}")
        language = user.language if user else "ru"
        await callback.answer(get_text("error", language), show_alert=True)


@router.callback_query(F.data == "admin_daily_reports", IsAdminFilter())
async def admin_daily_reports(callback: CallbackQuery, user: User, session: AsyncSession):
    """Показать отчеты за сегодня"""
    try:
        language = user.language if user else "ru"
        
        today = date.today()
        start_date = datetime.combine(today, datetime.min.time())
        end_date = datetime.combine(today, datetime.max.time())
        
        users = await UserRepository.get_all_active(session)
        reports = await DailyReportRepository.get_reports_by_date_range(
            session,
            start_date,
            end_date
        )
        
        total_users = len(users)
        submitted_reports = len(reports)
        no_tasks_count = sum(1 for r in reports if not r.has_tasks)
        not_submitted = total_users - submitted_reports
        
        details = "👥 Подробности / Təfərrüatlar:\n\n"
        
        details += "✅ С задачами / Tapşırıqlarla:\n"
        for report in reports:
            if report.has_tasks:
                u = next((user for user in users if user.telegram_id == report.telegram_id), None)
                if u:
                    details += f"  • {u.first_name} {u.last_name}\n"
        
        if no_tasks_count > 0:
            details += "\n🚫 Без задач / Tapşırıqsız:\n"
            for report in reports:
                if not report.has_tasks:
                    u = next((user for user in users if user.telegram_id == report.telegram_id), None)
                    if u:
                        details += f"  • {u.first_name} {u.last_name}\n"
        
        if not_submitted > 0:
            details += "\n❌ Не отправили / Göndərmədi:\n"
            submitted_ids = {r.telegram_id for r in reports}
            for u in users:
                if u.telegram_id not in submitted_ids:
                    details += f"  • {u.first_name} {u.last_name}\n"
        
        text = get_text(
            "daily_report_summary",
            language,
            date=today.strftime("%d.%m.%Y"),
            total=total_users,
            submitted=submitted_reports,
            not_submitted=not_submitted,
            no_tasks=no_tasks_count,
            details=details
        )
        
        await callback.message.edit_text(text)
        await callback.answer()
        
        logger.info(f"Администратор {callback.from_user.id} просмотрел ежедневные отчеты")
    
    except Exception as e:
        logger.error(f"Ошибка показа ежедневных отчетов: {e}")
        language = user.language if user else "ru"
        await callback.answer(get_text("error", language), show_alert=True)


@router.callback_query(F.data == "admin_weekly_report", IsAdminFilter())
async def admin_weekly_report(callback: CallbackQuery, user: User, session: AsyncSession):
    """Генерация недельного отчета"""
    try:
        language = user.language if user else "ru"
        admin_id = callback.from_user.id
        
        if admin_id in generating_reports:
            time_diff = (datetime.now() - generating_reports[admin_id]).total_seconds()
            if time_diff < 120:
                await callback.answer(
                    "⏳ Отчет уже формируется, подождите...\n"
                    "Hesabat artıq hazırlanır, gözləyin..." if language == "az" else 
                    "⏳ Отчет уже формируется, подождите...",
                    show_alert=True
                )
                return
            else:
                del generating_reports[admin_id]
        
        generating_reports[admin_id] = datetime.now()
        
        loading_text = (
            "⏳ Həftəlik hesabat hazırlanır...\nBu 1 dəqiqəyə qədər çəkə bilər."
            if language == "az" else
            "⏳ Формирую недельный отчет...\nЭто может занять до 1 минуты."
        )
        loading_msg = await callback.message.answer(loading_text)
        await callback.answer()
        
        today = date.today()
        week_start = today - timedelta(days=today.weekday())
        week_end = today
        
        start_datetime = datetime.combine(week_start, datetime.min.time())
        end_datetime = datetime.combine(week_end, datetime.max.time())
        
        reports = await DailyReportRepository.get_reports_by_date_range(
            session,
            start_datetime,
            end_datetime
        )
        
        if not reports:
            del generating_reports[admin_id]
            await loading_msg.delete()
            no_data_text = (
                "📭 Bu həftə hesabat yoxdur"
                if language == "az" else
                "📭 Нет отчетов за эту неделю"
            )
            await callback.message.answer(no_data_text)
            return
        
        users = await UserRepository.get_all_active(session)
        user_dict = {u.telegram_id: u for u in users}
        
        reports_data = []
        for report in reports:
            u = user_dict.get(report.telegram_id)
            if u:
                reports_data.append({
                    'date': report.report_date,
                    'first_name': u.first_name,
                    'last_name': u.last_name,
                    'report_text': report.report_text,
                    'has_tasks': report.has_tasks
                })
        
        report_text = await deepseek_service.generate_weekly_report(
            reports_data,
            language=language
        )
        
        formatted_text = format_answer(report_text)
        
        week_start_str = week_start.strftime("%d.%m.%Y")
        week_end_str = week_end.strftime("%d.%m.%Y")
        
        docx_file = document_service.generate_docx(
            report_text,
            week_start_str,
            week_end_str
        )
        
        await loading_msg.delete()
        
        header = get_text("weekly_report_header", language, 
                         week_start=week_start_str, week_end=week_end_str)
        
        await callback.message.answer(
            f"{header}\n\n{formatted_text}",
            parse_mode="HTML"
        )
        
        await callback.message.answer_document(
            document=BufferedInputFile(
                docx_file.read(),
                filename=f"weekly_report_{week_start_str}_{week_end_str}.docx"
            ),
            caption="📄 DOCX версия отчета" if language == "ru" else "📄 Hesabatın DOCX versiyası"
        )
        
        del generating_reports[admin_id]
        
        logger.info(f"Администратор {callback.from_user.id} сгенерировал недельный отчет")
    
    except Exception as e:
        logger.error(f"Ошибка генерации недельного отчета: {e}")
        
        if callback.from_user.id in generating_reports:
            del generating_reports[callback.from_user.id]
        
        language = user.language if user else "ru"
        await callback.message.answer(get_text("error", language))


@router.message(Command("debug_notify"), IsAdminFilter())
async def debug_notify(message: Message, user: User):
    """DEBUG: Принудительно разослать уведомления"""
    try:
        from aiogram import Bot
        bot: Bot = message.bot
        sched = SchedulerService(bot)
        await sched._send_daily_notifications("9:00-18:00")
        await sched._send_daily_notifications("10:00-19:00")
        await sched._send_hourly_reminders()
        await message.answer("✅ debug_notify: отправлено")
    except Exception as e:
        await message.answer(f"❌ debug_notify ошибка: {e}")


@router.message(Command("debug_admin_daily"), IsAdminFilter())
async def debug_admin_daily(message: Message, user: User):
    """DEBUG: Ежедневный отчет админу"""
    try:
        from aiogram import Bot
        bot: Bot = message.bot
        sched = SchedulerService(bot)
        await sched._send_daily_admin_report()
        await message.answer("✅ admin daily sent")
    except Exception as e:
        await message.answer(f"❌ admin daily error: {e}")


@router.message(Command("debug_weekly"), IsAdminFilter())
async def debug_weekly(message: Message, user: User):
    """DEBUG: Недельный отчет"""
    try:
        from aiogram import Bot
        bot: Bot = message.bot
        sched = SchedulerService(bot)
        await sched._send_weekly_report()
        await message.answer("✅ weekly sent")
    except Exception as e:
        await message.answer(f"❌ weekly error: {e}")