"""
Клавиатуры - С ФУНКЦИЕЙ УДАЛЕНИЯ ПОЛЬЗОВАТЕЛЕЙ
"""
from typing import List
from aiogram.types import InlineKeyboardMarkup, ReplyKeyboardRemove
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder


def get_language_keyboard() -> InlineKeyboardMarkup:
    """Выбор языка"""
    builder = InlineKeyboardBuilder()
    builder.button(text="🇦🇿 Azərbaycanca", callback_data="lang_az")
    builder.button(text="🇷🇺 Русский", callback_data="lang_ru")
    builder.adjust(1)
    return builder.as_markup()


def get_work_time_keyboard(language: str = "ru") -> InlineKeyboardMarkup:
    """Выбор рабочего времени ДЛЯ РЕГИСТРАЦИИ"""
    texts = {
        "ru": {"morning": "🌅 9:00 - 18:00", "afternoon": "🌆 10:00 - 19:00", "back": "◀️ Назад"},
        "az": {"morning": "🌅 9:00 - 18:00", "afternoon": "🌆 10:00 - 19:00", "back": "◀️ Geri"}
    }
    builder = InlineKeyboardBuilder()
    builder.button(text=texts[language]["morning"], callback_data="work_time_9-18")
    builder.button(text=texts[language]["afternoon"], callback_data="work_time_10-19")
    builder.button(text=texts[language]["back"], callback_data="back_to_last_name")
    builder.adjust(1)
    return builder.as_markup()


def get_work_time_keyboard_for_profile(language: str = "ru") -> InlineKeyboardMarkup:
    """Выбор рабочего времени ДЛЯ ПРОФИЛЯ"""
    texts = {
        "ru": {"morning": "🌅 9:00 - 18:00", "afternoon": "🌆 10:00 - 19:00", "back": "◀️ Назад"},
        "az": {"morning": "🌅 9:00 - 18:00", "afternoon": "🌆 10:00 - 19:00", "back": "◀️ Geri"}
    }
    builder = InlineKeyboardBuilder()
    builder.button(text=texts[language]["morning"], callback_data="work_time_9-18")
    builder.button(text=texts[language]["afternoon"], callback_data="work_time_10-19")
    builder.button(text=texts[language]["back"], callback_data="back_to_profile")
    builder.adjust(1)
    return builder.as_markup()


def get_confirmation_keyboard(language: str = "ru") -> InlineKeyboardMarkup:
    """Подтверждение регистрации"""
    texts = {
        "ru": {"confirm": "✅ Подтвердить", "edit": "✏️ Изменить"},
        "az": {"confirm": "✅ Təsdiq et", "edit": "✏️ Dəyişdir"},
    }
    builder = InlineKeyboardBuilder()
    builder.button(text=texts[language]["confirm"], callback_data="confirm_yes")
    builder.button(text=texts[language]["edit"], callback_data="confirm_edit")
    builder.adjust(1)
    return builder.as_markup()


def get_report_type_keyboard(language: str = "ru") -> InlineKeyboardMarkup:
    """Выбор типа отчета"""
    texts = {
        "ru": {"has_tasks": "📝 Есть задачи для отчета", "no_tasks": "🚫 Задач не было"},
        "az": {"has_tasks": "📝 Hesabat üçün tapşırıqlar var", "no_tasks": "🚫 Tapşırıq olmayıb"},
    }
    builder = InlineKeyboardBuilder()
    builder.button(text=texts[language]["has_tasks"], callback_data="report_has_tasks")
    builder.button(text=texts[language]["no_tasks"], callback_data="report_no_tasks")
    builder.adjust(1)
    return builder.as_markup()


def get_cancel_and_examples_keyboard(language: str = "ru") -> InlineKeyboardMarkup:
    """Кнопки отмены и примеров при отправке отчета"""
    texts = {
        "ru": {"cancel": "❌ Отменить", "examples": "📝 Примеры"},
        "az": {"cancel": "❌ Ləğv et", "examples": "📝 Nümunələr"}
    }
    builder = InlineKeyboardBuilder()
    builder.button(text=texts[language]["examples"], callback_data="show_examples")
    builder.button(text=texts[language]["cancel"], callback_data="cancel_report")
    builder.adjust(2)
    return builder.as_markup()


def get_examples_keyboard(language: str = "ru") -> InlineKeyboardMarkup:
    """Клавиатура с примерами профессий"""
    texts = {
        "ru": {
            "uiux": "🎨 UI/UX Дизайнер",
            "graphic": "🖼 Графический дизайнер",
            "backend": "⚙️ PHP Backend",
            "flutter": "📱 Flutter Dev",
            "seo": "🔍 SEO",
            "back": "◀️ Назад"
        },
        "az": {
            "uiux": "🎨 UI/UX Dizayner",
            "graphic": "🖼 Qrafik dizayner",
            "backend": "⚙️ PHP Backend",
            "flutter": "📱 Flutter Dev",
            "seo": "🔍 SEO",
            "back": "◀️ Geri"
        }
    }
    builder = InlineKeyboardBuilder()
    builder.button(text=texts[language]["uiux"], callback_data="example_uiux")
    builder.button(text=texts[language]["graphic"], callback_data="example_graphic")
    builder.button(text=texts[language]["backend"], callback_data="example_backend")
    builder.button(text=texts[language]["flutter"], callback_data="example_flutter")
    builder.button(text=texts[language]["seo"], callback_data="example_seo")
    builder.button(text=texts[language]["back"], callback_data="back_to_report")
    builder.adjust(2, 2, 1, 1)
    return builder.as_markup()


def get_main_menu_keyboard(language: str = "ru", is_admin: bool = False):
    """Главное меню"""
    if not is_admin:
        return ReplyKeyboardRemove()
    
    texts = {
        "ru": {"admin": "⚙️ Админ-панель"},
        "az": {"admin": "⚙️ Admin panel"},
    }
    builder = ReplyKeyboardBuilder()
    builder.button(text=texts[language]["admin"])
    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True)


def get_edit_profile_keyboard(language: str = "ru") -> InlineKeyboardMarkup:
    """Редактирование профиля"""
    texts = {
        "ru": {"first_name": "✏️ Изменить имя", "last_name": "✏️ Изменить фамилию",
               "work_time": "⏰ Изменить время работы", "language": "🌐 Изменить язык",
               "back": "◀️ Назад"},
        "az": {"first_name": "✏️ Adı dəyişdir", "last_name": "✏️ Soyadı dəyişdir",
               "work_time": "⏰ İş vaxtını dəyişdir", "language": "🌐 Dili dəyişdir",
               "back": "◀️ Geri"},
    }
    builder = InlineKeyboardBuilder()
    builder.button(text=texts[language]["first_name"], callback_data="edit_first_name")
    builder.button(text=texts[language]["last_name"], callback_data="edit_last_name")
    builder.button(text=texts[language]["work_time"], callback_data="edit_work_time")
    builder.button(text=texts[language]["language"], callback_data="edit_language")
    builder.button(text=texts[language]["back"], callback_data="back_to_menu")
    builder.adjust(1)
    return builder.as_markup()


def get_admin_keyboard(language: str = "ru") -> InlineKeyboardMarkup:
    """Админ-панель"""
    texts = {
        "ru": {"stats": "📊 Статистика", "users": "👥 Пользователи",
               "reports": "📋 Отчеты за сегодня", "weekly": "📅 Недельный отчет"},
        "az": {"stats": "📊 Statistika", "users": "👥 İstifadəçilər",
               "reports": "📋 Bugünkü hesabatlar", "weekly": "📅 Həftəlik hesabat"},
    }
    builder = InlineKeyboardBuilder()
    builder.button(text=texts[language]["stats"], callback_data="admin_stats")
    builder.button(text=texts[language]["users"], callback_data="admin_users")
    builder.button(text=texts[language]["reports"], callback_data="admin_daily_reports")
    builder.button(text=texts[language]["weekly"], callback_data="admin_weekly_report")
    builder.adjust(2)
    return builder.as_markup()


def get_user_list_keyboard(users: List, language: str, current_admin_id: int) -> InlineKeyboardMarkup:
    """
    ✅ НОВОЕ: Клавиатура списка пользователей с кнопками удаления
    """
    texts = {
        "ru": {"back": "◀️ Назад"},
        "az": {"back": "◀️ Geri"}
    }
    
    builder = InlineKeyboardBuilder()
    
    # Добавляем кнопки удаления для каждого пользователя
    for user in users:
        # Нельзя удалить себя или других админов
        if user.telegram_id == current_admin_id or user.is_admin:
            continue
            
        button_text = f"🗑 {user.first_name} {user.last_name}"
        builder.button(text=button_text, callback_data=f"delete_user_{user.telegram_id}")
    
    # Кнопка "Назад"
    builder.button(text=texts[language]["back"], callback_data="admin_panel_back")
    
    # Располагаем по 1 кнопке в ряд
    builder.adjust(1)
    
    return builder.as_markup()


def get_delete_confirmation_keyboard(telegram_id: int, language: str) -> InlineKeyboardMarkup:
    """
    ✅ НОВОЕ: Клавиатура подтверждения удаления пользователя
    """
    texts = {
        "ru": {"confirm": "✅ Да, удалить", "cancel": "❌ Отменить"},
        "az": {"confirm": "✅ Bəli, sil", "cancel": "❌ Ləğv et"}
    }
    
    builder = InlineKeyboardBuilder()
    builder.button(text=texts[language]["confirm"], callback_data=f"confirm_delete_{telegram_id}")
    builder.button(text=texts[language]["cancel"], callback_data=f"cancel_delete_{telegram_id}")
    builder.adjust(1)
    
    return builder.as_markup()