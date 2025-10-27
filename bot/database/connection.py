
"""
Настройка асинхронного подключения к базе данных (SQLAlchemy + aiomysql)
"""
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase
from loguru import logger
from config.settings import settings


class Base(DeclarativeBase):
    """Базовый класс для моделей SQLAlchemy"""
    pass


class DatabaseManager:
    """Менеджер для работы с БД и создания сессий"""

    def __init__(self):
        # Подключение к БД (настройки берём из .env через settings)
        self.engine = create_async_engine(
            settings.database_url,
            echo=False,
            future=True,
            pool_pre_ping=True,
            pool_size=10,
            max_overflow=20,
        )
        self.async_session = async_sessionmaker(
            self.engine,
            expire_on_commit=False,
            class_=AsyncSession,
        )

    async def create_tables(self):
        """Создание таблиц при запуске"""
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("Таблицы базы данных успешно созданы")

    @asynccontextmanager
    async def session(self):
        """
        Контекстный менеджер для удобной работы:
        async with db_manager.session() as session:
            ...
        """
        async with self.async_session() as session:
            try:
                yield session
            except Exception as e:
                await session.rollback()
                logger.error(f"Ошибка в сессии БД: {e}")
                raise
            finally:
                await session.close()

    async def get_session(self):
        """
        Старый способ — совместимость.
        Используется как async for session in db_manager.get_session()
        """
        async with self.session() as s:
            yield s


# Создаём экземпляр менеджера
db_manager = DatabaseManager()
