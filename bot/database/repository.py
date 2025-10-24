"""
Паттерн Repository для операций с базой данных
"""
from typing import Optional, List
from datetime import datetime, date, timedelta
from sqlalchemy import select, and_, update
from sqlalchemy.ext.asyncio import AsyncSession
from loguru import logger

from .models import User, DailyReport, WeeklyReport


class UserRepository:
    """Репозиторий для операций с пользователями"""

    @staticmethod
    async def get_by_telegram_id(session: AsyncSession, telegram_id: int) -> Optional[User]:
        """Получить пользователя по telegram ID"""
        try:
            stmt = select(User).where(User.telegram_id == telegram_id)
            return await session.scalar(stmt)
        except Exception as e:
            logger.error(f"Ошибка получения пользователя по telegram_id {telegram_id}: {e}")
            raise

    @staticmethod
    async def create(
        session: AsyncSession,
        telegram_id: int,
        first_name: str,
        last_name: str,
        language: str,
        work_time: str,
        is_admin: bool = False
    ) -> User:
        """Создать нового пользователя"""
        try:
            user = User(
                telegram_id=telegram_id,
                first_name=first_name,
                last_name=last_name,
                language=language,
                work_time=work_time,
                is_admin=is_admin,
            )
            session.add(user)
            await session.commit()
            await session.refresh(user)
            logger.info(f"Создан новый пользователь: {telegram_id}")
            return user
        except Exception as e:
            await session.rollback()
            logger.error(f"Ошибка создания пользователя {telegram_id}: {e}")
            raise

    @staticmethod
    async def update(session: AsyncSession, telegram_id: int, **kwargs) -> Optional[User]:
        """Обновить данные пользователя"""
        try:
            user = await UserRepository.get_by_telegram_id(session, telegram_id)
            if not user:
                return None

            for key, value in kwargs.items():
                if hasattr(user, key):
                    setattr(user, key, value)

            await session.commit()
            await session.refresh(user)
            logger.info(f"Обновлен пользователь {telegram_id}")
            return user
        except Exception as e:
            await session.rollback()
            logger.error(f"Ошибка обновления пользователя {telegram_id}: {e}")
            raise

    @staticmethod
    async def get_all_active(session: AsyncSession) -> List[User]:
        """Получить всех активных пользователей"""
        try:
            stmt = select(User).where(User.is_active == True)
            result = await session.scalars(stmt)
            return list(result)
        except Exception as e:
            logger.error(f"Ошибка получения всех активных пользователей: {e}")
            raise

    @staticmethod
    async def get_users_by_work_time(session: AsyncSession, work_time: str) -> List[User]:
        """Получить пользователей по рабочему времени"""
        try:
            stmt = select(User).where(and_(User.is_active == True, User.work_time == work_time))
            result = await session.scalars(stmt)
            return list(result)
        except Exception as e:
            logger.error(f"Ошибка получения пользователей по рабочему времени {work_time}: {e}")
            raise


class DailyReportRepository:
    """Репозиторий для ежедневных отчётов"""

    @staticmethod
    async def create(
        session: AsyncSession,
        user_id: int,
        telegram_id: int,
        report_date: datetime,
        report_text: Optional[str],
        has_tasks: bool,
    ) -> DailyReport:
        try:
            report = DailyReport(
                user_id=user_id,
                telegram_id=telegram_id,
                report_date=report_date,
                report_text=report_text,
                has_tasks=has_tasks,
            )
            session.add(report)
            await session.commit()
            await session.refresh(report)
            logger.info(f"Создан ежедневный отчёт для пользователя {telegram_id}")
            return report
        except Exception as e:
            await session.rollback()
            logger.error(f"Ошибка создания ежедневного отчёта: {e}")
            raise

    @staticmethod
    async def get_by_date(session: AsyncSession, telegram_id: int, report_date: date) -> Optional[DailyReport]:
        """Получить отчёт по пользователю и дате"""
        try:
            start_date = datetime.combine(report_date, datetime.min.time())
            end_date = datetime.combine(report_date, datetime.max.time())
            stmt = select(DailyReport).where(
                and_(
                    DailyReport.telegram_id == telegram_id,
                    DailyReport.report_date >= start_date,
                    DailyReport.report_date <= end_date,
                )
            )
            return await session.scalar(stmt)
        except Exception as e:
            logger.error(f"Ошибка получения отчёта для пользователя {telegram_id}: {e}")
            raise

    @staticmethod
    async def increment_reminder_count(session: AsyncSession, telegram_id: int, report_date: date) -> None:
        """Увеличить счётчик напоминаний"""
        try:
            start_date = datetime.combine(report_date, datetime.min.time())
            end_date = datetime.combine(report_date, datetime.max.time())
            await session.execute(
                update(DailyReport)
                .where(
                    and_(
                        DailyReport.telegram_id == telegram_id,
                        DailyReport.report_date >= start_date,
                        DailyReport.report_date <= end_date,
                    )
                )
                .values(reminder_count=DailyReport.reminder_count + 1)
            )
            await session.commit()
        except Exception as e:
            await session.rollback()
            logger.error(f"Ошибка увеличения reminder_count: {e}")
            raise


class WeeklyReportRepository:
    """Репозиторий для недельных отчётов"""

    @staticmethod
    async def create(session: AsyncSession, week_start: datetime, week_end: datetime, report_text: str) -> WeeklyReport:
        try:
            report = WeeklyReport(week_start=week_start, week_end=week_end, report_text=report_text)
            session.add(report)
            await session.commit()
            await session.refresh(report)
            logger.info(f"Создан недельный отчёт {week_start} - {week_end}")
            return report
        except Exception as e:
            await session.rollback()
            logger.error(f"Ошибка создания недельного отчёта: {e}")
            raise

    @staticmethod
    async def get_latest(session: AsyncSession) -> Optional[WeeklyReport]:
        try:
            stmt = select(WeeklyReport).order_by(WeeklyReport.created_at.desc()).limit(1)
            return await session.scalar(stmt)
        except Exception as e:
            logger.error(f"Ошибка получения последнего недельного отчёта: {e}")
            raise
