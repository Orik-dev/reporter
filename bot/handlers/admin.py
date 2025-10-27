"""
Обработчики для админ-панели - ФИНАЛЬНАЯ ВЕРСИЯ (исправлены двойные тексты)
"""
from datetime import date, datetime, timedelta
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, BufferedInputFile
from sqlalchemy.ext.asyncio import AsyncSession
from loguru import logger

from bot.keyboards import get_admin_keyboard
from bot.utils import get_text, format_answer
from bot.database import User, UserRepository, DailyReportRepository
from bot.filters import IsAdminFilter, IsNotAdminFilter
from bot.services import deepseek_service, document_service
from bot.services.scheduler_service import SchedulerService

router = Router()

# ✅ НОВОЕ: Хранилище для отслеживания генерации отчетов
generating_reports = {}  # {admin_id: datetime}


@router.message(Command("admin"), IsAdminFilter())
@router.message(F.text.in_(["⚙️ Админ-панель", "⚙️ Admin panel"]), IsAdminFilter())
async def cmd_admin(message: Message, user: User):
    """Админ-панель"""
    try:
        text = get_text("admin_panel", user.language if user else "ru")
        keyboard = get_admin_keyboard(user.language if user else "ru")
        
        await message.answer(text, reply_markup=keyboard)
        
        logger.info(f"✅ Администратор {message.from_user.id} открыл админ-панель")
    
    except Exception as e:
        logger.error(f"Ошибка в команде admin: {e}")
        await message.answer(get_text("error", user.language if user else "ru"))


@router.message(Command("admin"), IsNotAdminFilter())
@router.message(F.text.in_(["⚙️ Админ-панель", "⚙️ Admin panel"]), IsNotAdminFilter())
async def cmd_admin_not_authorized(message: Message, user: User):
    """Попытка доступа без прав"""
    try:
        text = get_text("not_authorized", user.language if user else "ru")
        await message.answer(text)
        
        logger.warning(f"⚠️ Пользователь {message.from_user.id} попытался войти в админ-панель без прав")
    
    except Exception as e:
        logger.error(f"Ошибка в admin not authorized: {e}")


@router.callback_query(F.data == "admin_stats", IsAdminFilter())
async def admin_stats(callback: CallbackQuery, user: User, session: AsyncSession):
    """Показать статистику"""
    try:
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
            user.language if user else "ru",
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
        await callback.answer(get_text("error", user.language if user else "ru"), show_alert=True)


@router.callback_query(F.data == "admin_users", IsAdminFilter())
async def admin_users(callback: CallbackQuery, user: User, session: AsyncSession):
    """Показать список пользователей"""
    try:
        users = await UserRepository.get_all_active(session)
        
        users_text = ""
        for u in users:
            admin_badge = " 👑" if u.is_admin else ""
            users_text += f"• {u.first_name} {u.last_name} ({u.work_time}){admin_badge}\n"
        
        text = get_text(
            "user_list",
            user.language if user else "ru",
            count=len(users),
            users=users_text
        )
        
        await callback.message.edit_text(text)
        await callback.answer()
        
        logger.info(f"Администратор {callback.from_user.id} просмотрел список пользователей")
    
    except Exception as e:
        logger.error(f"Ошибка показа пользователей: {e}")
        await callback.answer(get_text("error", user.language if user else "ru"), show_alert=True)


@router.callback_query(F.data == "admin_daily_reports", IsAdminFilter())
async def admin_daily_reports(callback: CallbackQuery, user: User, session: AsyncSession):
    """Показать отчеты за сегодня"""
    try:
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
            user.language if user else "ru",
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
        await callback.answer(get_text("error", user.language if user else "ru"), show_alert=True)


@router.callback_query(F.data == "admin_weekly_report", IsAdminFilter())
async def admin_weekly_report(callback: CallbackQuery, user: User, session: AsyncSession):
    """
    ✅ ФИНАЛЬНАЯ ВЕРСИЯ: Генерация недельного отчета
    """
    try:
        admin_id = callback.from_user.id
        
        # Проверяем, не формируется ли уже отчет
        if admin_id in generating_reports:
            time_diff = (datetime.now() - generating_reports[admin_id]).total_seconds()
            if time_diff < 120:
                await callback.answer(
                    "⏳ Отчет уже формируется, подождите...\n"
                    "Hesabat artıq hazırlanır, gözləyin..." if user.language == "az" else 
                    "⏳ Отчет уже формируется, подождите...",
                    show_alert=True
                )
                return
            else:
                del generating_reports[admin_id]
        
        # Отмечаем начало генерации
        generating_reports[admin_id] = datetime.now()
        
        # ✅ ИСПРАВЛЕНО: Показываем индикатор загрузки только на языке админа
        loading_text = (
            "⏳ Həftəlik hesabat hazırlanır...\nBu 1 dəqiqəyə qədər çəkə bilər."
            if user.language == "az" else
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
                if user.language == "az" else
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
        
        # Генерируем отчет с AI
        report_text = await deepseek_service.generate_weekly_report(
            reports_data,
            language=user.language
        )
        
        # ✅ ИСПРАВЛЕНО: Форматируем текст для Telegram
        formatted_text = format_answer(report_text)
        
        week_start_str = week_start.strftime("%d.%m.%Y")
        week_end_str = week_end.strftime("%d.%m.%Y")
        
        # Генерируем документы
        docx_file = document_service.generate_docx(
            report_text,
            week_start_str,
            week_end_str
        )
        
        pdf_file = document_service.generate_pdf(
            report_text,
            week_start_str,
            week_end_str
        )
        
        # Удаляем сообщение о загрузке
        await loading_msg.delete()
        
        # ✅ ИСПРАВЛЕНО: Отправляем заголовок и текст на языке админа
        header = get_text("weekly_report_header", user.language, 
                         week_start=week_start_str, week_end=week_end_str)
        
        await callback.message.answer(
            f"{header}\n\n{formatted_text}",
            parse_mode="HTML"
        )
        
        # Отправляем DOCX
        await callback.message.answer_document(
            document=BufferedInputFile(
                docx_file.read(),
                filename=f"weekly_report_{week_start_str}_{week_end_str}.docx"
            ),
            caption="📄 DOCX версия отчета" if user.language == "ru" else "📄 Hesabatın DOCX versiyası"
        )
        
        # Отправляем PDF
        pdf_file.seek(0)
        await callback.message.answer_document(
            document=BufferedInputFile(
                pdf_file.read(),
                filename=f"weekly_report_{week_start_str}_{week_end_str}.pdf"
            ),
            caption="📄 PDF версия отчета" if user.language == "ru" else "📄 Hesabatın PDF versiyası"
        )
        
        # Удаляем из generating_reports
        del generating_reports[admin_id]
        
        logger.info(f"Администратор {callback.from_user.id} сгенерировал недельный отчет")
    
    except Exception as e:
        logger.error(f"Ошибка генерации недельного отчета: {e}")
        
        if callback.from_user.id in generating_reports:
            del generating_reports[callback.from_user.id]
        
        await callback.message.answer(get_text("error", user.language if user else "ru"))


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
