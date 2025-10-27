"""
Модели базы данных с использованием SQLAlchemy ORM
"""
from datetime import datetime
from typing import Optional
from sqlalchemy import BigInteger, String, DateTime, Boolean, Text, Integer, Enum
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
import enum


class Base(DeclarativeBase):
    pass


class LanguageEnum(enum.Enum):
    AZ = "az"
    RU = "ru"


class WorkTimeEnum(enum.Enum):
    MORNING = "9:00-18:00"
    AFTERNOON = "10:00-19:00"


class User(Base):
    __tablename__ = 'users'
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False, index=True)
    first_name: Mapped[str] = mapped_column(String(255), nullable=False)
    last_name: Mapped[str] = mapped_column(String(255), nullable=False)
    language: Mapped[str] = mapped_column(String(2), nullable=False)  # 'az' или 'ru'
    work_time: Mapped[str] = mapped_column(String(20), nullable=False)  # '9:00-18:00' или '10:00-19:00'
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )
    
    def __repr__(self) -> str:
        return f"<User(id={self.id}, telegram_id={self.telegram_id}, name={self.first_name} {self.last_name})>"


class DailyReport(Base):
    __tablename__ = 'daily_reports'
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger, nullable=False, index=True)
    report_date: Mapped[datetime] = mapped_column(DateTime, nullable=False, index=True)
    report_text: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    has_tasks: Mapped[bool] = mapped_column(Boolean, nullable=False)  # True если были задачи, False если нет
    submitted_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    reminder_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)  # Количество отправленных напоминаний
    
    def __repr__(self) -> str:
        return f"<DailyReport(id={self.id}, user_id={self.user_id}, date={self.report_date})>"


class WeeklyReport(Base):
    __tablename__ = 'weekly_reports'
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    week_start: Mapped[datetime] = mapped_column(DateTime, nullable=False, index=True)
    week_end: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    report_text: Mapped[str] = mapped_column(Text, nullable=False)  # AI-сгенерированный отчет
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    
    def __repr__(self) -> str:
        return f"<WeeklyReport(id={self.id}, week={self.week_start} - {self.week_end})>"