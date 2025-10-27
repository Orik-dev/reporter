"""
Планировщик задач - ИСПРАВЛЕННАЯ ВЕРСИЯ
"""
from datetime import datetime, timedelta, date
import pytz
from typing import List, Dict
from loguru import logger
from aiogram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger

from config.settings import settings
from bot.database import db_manager, UserRepository, DailyReportRepository
from bot.utils import get_text
from bot.keyboards import get_report_type_keyboard
from bot.services.deepseek_service import deepseek_service
from bot.services.document_service import document_service
from aiogram.types import BufferedInputFile


class SchedulerService:
    """Сервис для планирования периодических задач"""

    def __init__(self, bot: Bot):
        self.bot = bot
        self.timezone = pytz.timezone(settings.timezone)
        self.scheduler = AsyncIOScheduler(
            timezone=self.timezone,
            job_defaults={
                "misfire_grace_time": settings.scheduler_misfire_grace,
                "coalesce": True,
                "max_instances": 1,
            },
        )
        # ✅ ДОБАВЛЕНО: Храним последнее время отправки напоминания каждому пользователю
        self.last_reminder_time: Dict[int, datetime] = {}

    def start(self):
        """Запустить планировщик"""
        now_baku = datetime.now(self.timezone).strftime("%Y-%m-%d %H:%M:%S %Z")
        logger.info(f"APScheduler starting, current Baku time: {now_baku}")

        self._schedule_daily_notifications()
        self._schedule_hourly_reminders()
        self._schedule_daily_admin_report()
        self._schedule_weekly_report()

        self.scheduler.start()
        logger.info("Планировщик успешно запущен")

    def shutdown(self):
        self.scheduler.shutdown()
        logger.info("Планировщик остановлен")

    def _schedule_daily_notifications(self):
        """Ежедневные уведомления в конце рабочего дня"""
        h1, m1 = map(int, settings.notification_time_1.split(':'))
        h2, m2 = map(int, settings.notification_time_2.split(':'))

        self.scheduler.add_job(
            self._send_daily_notifications,
            CronTrigger(hour=h1, minute=m1, timezone=self.timezone),
            args=["9:00-18:00"],
            id='notification_9_18'
        )

        self.scheduler.add_job(
            self._send_daily_notifications,
            CronTrigger(hour=h2, minute=m2, timezone=self.timezone),
            args=["10:00-19:00"],
            id='notification_10_19'
        )
        logger.info(f"Ежедневные уведомления запланированы на {settings.notification_time_1} и {settings.notification_time_2} (Baku)")

    def _schedule_hourly_reminders(self):
        """Ежечасные напоминания (интервал)"""
        self.scheduler.add_job(
            self._send_hourly_reminders,
            IntervalTrigger(minutes=settings.reminder_interval_minutes, timezone=self.timezone),
            id='hourly_reminders'
        )
        logger.info(f"Ежечасные напоминания каждые {settings.reminder_interval_minutes} мин.")

    def _schedule_daily_admin_report(self):
        """Ежедневный отчёт админу в 23:59"""
        self.scheduler.add_job(
            self._send_daily_admin_report,
            CronTrigger(hour=23, minute=59, timezone=self.timezone),
            id='daily_admin_report'
        )
        logger.info("Ежедневный отчёт админу запланирован на 23:59 (Baku).")

    def _schedule_weekly_report(self):
        """Недельный отчёт (пятница, 00:00 по Баку)"""
        hh, mm = map(int, settings.weekly_report_time.split(':'))
        self.scheduler.add_job(
            self._send_weekly_report,
            CronTrigger(day_of_week=settings.weekly_report_day, hour=hh, minute=mm, timezone=self.timezone),
            id='weekly_report'
        )
        logger.info(f"Недельный отчёт запланирован на день недели={settings.weekly_report_day} {settings.weekly_report_time} (Baku).")

    # ---------- задачи ----------

    async def _send_daily_notifications(self, work_time: str):
        """Пинг в конце рабочего дня: попросить отчёт"""
        try:
            async for session in db_manager.get_session():
                users = await UserRepository.get_users_by_work_time(session, work_time)
                today = date.today()

                for user in users:
                    if user.is_admin:
                        continue
                    # уже есть отчёт за сегодня?
                    existing = await DailyReportRepository.get_by_date(session, user.telegram_id, today)
                    if existing:
                        logger.info(f"[notify] {user.telegram_id} уже отправил отчёт сегодня — пропуск")
                        continue

                    try:
                        await self.bot.send_message(
                            chat_id=user.telegram_id,
                            text=get_text("report_request", user.language),
                            reply_markup=get_report_type_keyboard(user.language)
                        )
                        logger.info(f"[notify] отправлено уведомление пользователю {user.telegram_id} ({work_time})")
                    except Exception as tg_err:
                        logger.error(f"[notify] ошибка Telegram для {user.telegram_id}: {tg_err}")

        except Exception as e:
            logger.error(f"Ошибка в задаче уведомлений: {e}")

    async def _send_hourly_reminders(self):
        """
        ✅ ИСПРАВЛЕНО: Ежечасные напоминания с проверкой времени и частоты
        - Отправляются только после конца рабочего дня и до 23:00
        - Не чаще 1 раза в час одному пользователю
        - Не отправляются админам
        """
        try:
            now_baku = datetime.now(self.timezone)
            current_hour = now_baku.hour
            
            # ✅ ИСПРАВЛЕНО: Проверка верхней границы - не отправлять после 23:00
            if current_hour >= 23:
                logger.debug(f"[reminder] Время {current_hour}:00 - слишком поздно, пропуск")
                return
            
            async for session in db_manager.get_session():
                users = await UserRepository.get_all_active(session)
                today = date.today()
                
                for user in users:
                    # ✅ Не отправлять админам
                    if user.is_admin:
                        continue
                    
                    # Проверка, есть ли уже отчет
                    existing_report = await DailyReportRepository.get_by_date(session, user.telegram_id, today)
                    if existing_report:
                        logger.debug(f"[reminder] {user.telegram_id} уже отправил отчет, пропуск")
                        continue
                    
                    # ✅ Проверка времени: напоминания только после конца рабочего дня
                    end_hour = 18 if user.work_time == "9:00-18:00" else 19
                    if current_hour < end_hour:
                        logger.debug(
                            f"[reminder] {user.telegram_id} рабочий день не закончен "
                            f"(current={current_hour}, end={end_hour}), пропуск"
                        )
                        continue
                    
                    # ✅ ИСПРАВЛЕНО: Проверка частоты - не чаще раза в час
                    last_reminder = self.last_reminder_time.get(user.telegram_id)
                    if last_reminder:
                        time_since_last = (now_baku - last_reminder).total_seconds()
                        if time_since_last < 3600:  # Меньше часа
                            logger.debug(
                                f"[reminder] {user.telegram_id} недавно получил напоминание "
                                f"({time_since_last/60:.1f} мин назад), пропуск"
                            )
                            continue
                    
                    # Отправляем напоминание
                    try:
                        await self.bot.send_message(
                            chat_id=user.telegram_id,
                            text=get_text("reminder", user.language),
                            reply_markup=get_report_type_keyboard(user.language)
                        )
                        
                        # ✅ Обновляем время последнего напоминания
                        self.last_reminder_time[user.telegram_id] = now_baku
                        
                        logger.info(
                            f"[reminder] отправлено {user.telegram_id} "
                            f"(time={current_hour}:00, work_end={end_hour}:00)"
                        )
                    except Exception as tg_err:
                        logger.error(f"[reminder] ошибка Telegram для {user.telegram_id}: {tg_err}")

        except Exception as e:
            logger.error(f"Ошибка в задаче ежечасных напоминаний: {e}")

    async def _send_daily_admin_report(self):
        """Ежедневная сводка админу"""
        try:
            async for session in db_manager.get_session():
                today = date.today()
                start = datetime.combine(today, datetime.min.time())
                end = datetime.combine(today, datetime.max.time())

                users = await UserRepository.get_all_active(session)
                reports = await DailyReportRepository.get_reports_by_date_range(session, start, end)

                total = len(users)
                submitted = len(reports)
                no_tasks = sum(1 for r in reports if not r.has_tasks)
                not_submitted = total - submitted

                details = "👥 Подробности / Təfərrüatlar:\n\n"
                # с задачами
                details += "✅ С задачами / Tapşırıqlarla:\n"
                for r in reports:
                    if r.has_tasks:
                        u = next((x for x in users if x.telegram_id == r.telegram_id), None)
                        if u:
                            details += f"  • {u.first_name} {u.last_name}\n"
                # без задач
                if no_tasks:
                    details += "\n🚫 Без задач / Tapşırıqsız:\n"
                    for r in reports:
                        if not r.has_tasks:
                            u = next((x for x in users if x.telegram_id == r.telegram_id), None)
                            if u:
                                details += f"  • {u.first_name} {u.last_name}\n"
                # не отправили
                if not_submitted:
                    details += "\n❌ Не отправили / Göndərmədi:\n"
                    submitted_ids = {r.telegram_id for r in reports}
                    for u in users:
                        if u.telegram_id not in submitted_ids:
                            details += f"  • {u.first_name} {u.last_name}\n"

                for admin_id in settings.admin_ids_list:
                    try:
                        await self.bot.send_message(
                            chat_id=admin_id,
                            text=get_text(
                                "daily_report_summary",
                                "ru",
                                date=today.strftime("%d.%m.%Y"),
                                total=total,
                                submitted=submitted,
                                not_submitted=not_submitted,
                                no_tasks=no_tasks,
                                details=details
                            )
                        )
                        logger.info(f"[admin daily] отправлено админу {admin_id}")
                    except Exception as tg_err:
                        logger.error(f"[admin daily] ошибка Telegram для {admin_id}: {tg_err}")

        except Exception as e:
            logger.error(f"Ошибка в задаче ежедневного отчёта админу: {e}")

    async def _send_weekly_report(self):
        """Недельный отчёт админу (AI + DOCX/PDF)"""
        try:
            async for session in db_manager.get_session():
                today = date.today()
                week_start = today - timedelta(days=today.weekday())
                week_end = today

                start_dt = datetime.combine(week_start, datetime.min.time())
                end_dt = datetime.combine(week_end, datetime.max.time())

                reports = await DailyReportRepository.get_reports_by_date_range(session, start_dt, end_dt)
                if not reports:
                    logger.warning("[weekly] нет данных за неделю — пропуск")
                    return

                users = await UserRepository.get_all_active(session)
                user_map = {u.telegram_id: u for u in users}

                data = []
                for r in reports:
                    u = user_map.get(r.telegram_id)
                    if u:
                        data.append({
                            "date": r.report_date,
                            "first_name": u.first_name,
                            "last_name": u.last_name,
                            "report_text": r.report_text,
                            "has_tasks": r.has_tasks
                        })

                text = await deepseek_service.generate_weekly_report(data, language="ru")

                ws = week_start.strftime("%d.%m.%Y")
                we = week_end.strftime("%d.%m.%Y")

                docx_io = document_service.generate_docx(text, ws, we)
                pdf_io = document_service.generate_pdf(text, ws, we)

                for admin_id in settings.admin_ids_list:
                    try:
                        await self.bot.send_message(chat_id=admin_id, text=f"📊 Еженедельный отчет за {ws} - {we}")

                        docx_io.seek(0)
                        await self.bot.send_document(
                            chat_id=admin_id,
                            document=BufferedInputFile(docx_io.read(), filename=f"weekly_report_{ws}_{we}.docx")
                        )

                        pdf_io.seek(0)
                        await self.bot.send_document(
                            chat_id=admin_id,
                            document=BufferedInputFile(pdf_io.read(), filename=f"weekly_report_{ws}_{we}.pdf")
                        )
                        logger.info(f"[weekly] отправлено админу {admin_id}")
                    except Exception as tg_err:
                        logger.error(f"[weekly] ошибка Telegram для {admin_id}: {tg_err}")

        except Exception as e:
            logger.error(f"Ошибка в задаче недельного отчёта: {e}")