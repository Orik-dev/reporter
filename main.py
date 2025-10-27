"""
Main bot file
"""
import asyncio
import sys
from loguru import logger
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from config.settings import settings
from bot.database import db_manager
from bot.middlewares import (
    LoggingMiddleware,
    DatabaseMiddleware,
    UserCheckMiddleware,
    AdminCheckMiddleware,
    CallbackAgeMiddleware
)
from bot.handlers import start, reports, profile, admin, common
from bot.services import SchedulerService


# Configure logging
logger.remove()
logger.add(
    sys.stderr,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    level=settings.log_level
)
logger.add(
    settings.log_file,
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
    level=settings.log_level,
    rotation="10 MB",
    compression="zip",
    retention="30 days"
)


class RetryMiddleware:
    async def __call__(self, handler, event, data):
        max_retries = 2
        for attempt in range(max_retries + 1):
            try:
                return await handler(event, data)
            except TelegramBadRequest as e:
                if "query is too old" in str(e) or "timeout expired" in str(e):
                    if attempt == max_retries:
                        logger.error(f"Max retries reached for {event}: {e}")
                        raise
                    logger.warning(f"Retry {attempt + 1}/{max_retries} for {event}: {e}")
                    await asyncio.sleep(1)  # Задержка перед повторной попыткой
                else:
                    raise
        # Импорт внутри функции для избежания циклических зависимостей
        from aiogram.exceptions import TelegramBadRequest
        
async def on_startup(bot: Bot, scheduler: SchedulerService):
    """Actions on bot startup"""
    try:
        # Create database tables
        await db_manager.create_tables()
        logger.info("Database initialized")
        
        # Start scheduler
        scheduler.start()
        logger.info("Scheduler started")
        
        # Notify admins
        for admin_id in settings.admin_ids_list:
            try:
                await bot.send_message(
                    admin_id,
                    "🤖 Бот запущен и готов к работе!\n"
                    "Bot started and ready to work!"
                )
            except Exception as e:
                logger.warning(f"Could not notify admin {admin_id}: {e}")
        
        logger.info("Bot started successfully")
    
    except Exception as e:
        logger.error(f"Error on startup: {e}")
        raise


async def on_shutdown(bot: Bot, scheduler: SchedulerService):
    """Actions on bot shutdown"""
    try:
        # Stop scheduler
        scheduler.shutdown()
        logger.info("Scheduler stopped")
        
        # Notify admins
        for admin_id in settings.admin_ids_list:
            try:
                await bot.send_message(
                    admin_id,
                    "🤖 Бот остановлен\n"
                    "Bot stopped"
                )
            except Exception as e:
                logger.warning(f"Could not notify admin {admin_id}: {e}")
        
        logger.info("Bot shut down successfully")
    
    except Exception as e:
        logger.error(f"Error on shutdown: {e}")


async def main():
    """Main function"""
    try:
        # Initialize bot and dispatcher
        bot = Bot(
            token=settings.bot_token,
            timeout=60,
            default=DefaultBotProperties(parse_mode=ParseMode.HTML)
        )
        
        storage = MemoryStorage()
        dp = Dispatcher(storage=storage)
        
        # Initialize scheduler
        scheduler = SchedulerService(bot)
        
        # КРИТИЧНО: middleware в правильном порядке на OUTER уровне
        # Outer middleware выполняются ПЕРВЫМИ, до обработки роутеров
        dp.message.outer_middleware(DatabaseMiddleware())
        dp.message.outer_middleware(UserCheckMiddleware())
        dp.message.outer_middleware(AdminCheckMiddleware())
        
        dp.callback_query.outer_middleware(DatabaseMiddleware())
        dp.callback_query.outer_middleware(UserCheckMiddleware())
        dp.callback_query.outer_middleware(AdminCheckMiddleware())
        dp.callback_query.outer_middleware(CallbackAgeMiddleware())
        
        dp.message.middleware(RetryMiddleware())
        dp.callback_query.middleware(RetryMiddleware())
        # Logging middleware последним
        dp.message.middleware(LoggingMiddleware())
        dp.callback_query.middleware(LoggingMiddleware())
        
        # Register routers (порядок важен!)
        dp.include_router(start.router)
        dp.include_router(admin.router)
        dp.include_router(profile.router)
        dp.include_router(reports.router)
        dp.include_router(common.router)
        
        # Startup actions
        await on_startup(bot, scheduler)
        
        try:
            # Start polling
            logger.info("Starting bot polling...")
            await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
        
        finally:
            # Shutdown actions
            await on_shutdown(bot, scheduler)
    
    except Exception as e:
        logger.error(f"Critical error in main: {e}")
        sys.exit(1)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        sys.exit(1)