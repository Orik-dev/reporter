"""
Форматирование текста для Telegram
"""
import re
from chatgpt_md_converter import telegram_format


def format_answer(text: str) -> str:
    """
    Форматирует текст из DeepSeek для Telegram
    Использует chatgpt-md-converter
    """
    formatted = telegram_format(text)
    # Удаляем \ только перед неопасными символами
    formatted = re.sub(r'\\([a-zA-Z0-9\s.,!?\'"«»()\-])', r'\1', formatted)
    return formatted