"""
Application configuration using pydantic-settings
"""
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    """Application settings"""
    
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        case_sensitive=False
    )
    
    # Bot Configuration
    bot_token: str = Field(..., alias='BOT_TOKEN')
    admin_ids: str = Field(..., alias='ADMIN_IDS')
    
    # Database Configuration
    db_host: str = Field(default='localhost', alias='DB_HOST')
    db_port: int = Field(default=3306, alias='DB_PORT')
    db_user: str = Field(..., alias='DB_USER')
    db_password: str = Field(..., alias='DB_PASSWORD')
    db_name: str = Field(..., alias='DB_NAME')
    
    # DeepSeek API Configuration
    deepseek_api_key: str = Field(..., alias='DEEPSEEK_API_KEY')
    deepseek_api_url: str = Field(
        default='https://api.deepseek.com/v1/chat/completions',
        alias='DEEPSEEK_API_URL'
    )
    scheduler_start_kick_seconds: int = Field(default=0, alias="SCHEDULER_START_KICK_SECONDS")
    scheduler_misfire_grace: int = Field(default=300, alias="SCHEDULER_MISFIRE_GRACE")

    # Timezone
    timezone: str = Field(default='Asia/Baku', alias='TIMEZONE')
    
    # Scheduler Configuration
    notification_time_1: str = Field(default='18:00', alias='NOTIFICATION_TIME_1')
    notification_time_2: str = Field(default='19:00', alias='NOTIFICATION_TIME_2')
    reminder_interval_minutes: int = Field(default=60, alias='REMINDER_INTERVAL_MINUTES')
    weekly_report_day: int = Field(default=4, alias='WEEKLY_REPORT_DAY')
    weekly_report_time: str = Field(default='00:00', alias='WEEKLY_REPORT_TIME')
    
    # Logging
    log_level: str = Field(default='INFO', alias='LOG_LEVEL')
    log_file: str = Field(default='logs/bot.log', alias='LOG_FILE')
    
    @property
    def admin_ids_list(self) -> List[int]:
        """Convert admin IDs string to list of integers"""
        return [int(id_.strip()) for id_ in self.admin_ids.split(',') if id_.strip()]
    
    @property
    def database_url(self) -> str:
        """Generate database URL for SQLAlchemy"""
        return f"mysql+aiomysql://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"


# Create settings instance
settings = Settings()