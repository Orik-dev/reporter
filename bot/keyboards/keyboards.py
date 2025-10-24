# """
# Клавиатуры и кнопки для бота
# """
# from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
# from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder


# def get_language_keyboard() -> InlineKeyboardMarkup:
#     """Клавиатура для выбора языка"""
#     builder = InlineKeyboardBuilder()
#     builder.button(text="🇦🇿 Azərbaycanca", callback_data="lang_az")
#     builder.button(text="🇷🇺 Русский", callback_data="lang_ru")
#     builder.adjust(1)  # Одна кнопка в строке
#     return builder.as_markup()


# def get_work_time_keyboard(language: str = "ru") -> InlineKeyboardMarkup:
#     """Клавиатура для выбора рабочего времени"""
#     texts = {
#         "ru": {
#             "morning": "🌅 9:00 - 18:00",
#             "afternoon": "🌆 10:00 - 19:00"
#         },
#         "az": {
#             "morning": "🌅 9:00 - 18:00",
#             "afternoon": "🌆 10:00 - 19:00"
#         }
#     }
    
#     builder = InlineKeyboardBuilder()
#     builder.button(text=texts[language]["morning"], callback_data="work_time_9-18")
#     builder.button(text=texts[language]["afternoon"], callback_data="work_time_10-19")
#     builder.adjust(1)
#     return builder.as_markup()


# def get_confirmation_keyboard(language: str = "ru") -> InlineKeyboardMarkup:
#     """Клавиатура для подтверждения"""
#     texts = {
#         "ru": {
#             "confirm": "✅ Подтвердить",
#             "edit": "✏️ Изменить",
#             "cancel": "❌ Отменить"
#         },
#         "az": {
#             "confirm": "✅ Təsdiq et",
#             "edit": "✏️ Dəyişdir",
#             "cancel": "❌ Ləğv et"
#         }
#     }
    
#     builder = InlineKeyboardBuilder()
#     builder.button(text=texts[language]["confirm"], callback_data="confirm_yes")
#     builder.button(text=texts[language]["edit"], callback_data="confirm_edit")
#     builder.button(text=texts[language]["cancel"], callback_data="confirm_cancel")
#     builder.adjust(1)
#     return builder.as_markup()


# def get_cancel_keyboard(language: str = "ru") -> InlineKeyboardMarkup:
#     """Клавиатура с кнопкой отмены"""
#     texts = {
#         "ru": "❌ Отменить",
#         "az": "❌ Ləğv et"
#     }
    
#     builder = InlineKeyboardBuilder()
#     builder.button(text=texts[language], callback_data="cancel")
#     return builder.as_markup()


# def get_report_type_keyboard(language: str = "ru") -> InlineKeyboardMarkup:
#     """Клавиатура для выбора типа отчета (с задачами / без задач)"""
#     texts = {
#         "ru": {
#             "has_tasks": "📝 Есть задачи для отчета",
#             "no_tasks": "🚫 Задач не было"
#         },
#         "az": {
#             "has_tasks": "📝 Hesabat üçün tapşırıqlar var",
#             "no_tasks": "🚫 Tapşırıq olmayıb"
#         }
#     }
    
#     builder = InlineKeyboardBuilder()
#     builder.button(text=texts[language]["has_tasks"], callback_data="report_has_tasks")
#     builder.button(text=texts[language]["no_tasks"], callback_data="report_no_tasks")
#     builder.adjust(1)
#     return builder.as_markup()


# def get_main_menu_keyboard(language: str = "ru", is_admin: bool = False) -> ReplyKeyboardMarkup:
#     """Главное меню клавиатуры"""
#     texts = {
#         "ru": {
#             "profile": "👤 Мой профиль",
#             "report": "📊 Отправить отчет",
#             "help": "❓ Помощь",
#             "admin": "⚙️ Админ-панель"
#         },
#         "az": {
#             "profile": "👤 Mənim profilim",
#             "report": "📊 Hesabat göndər",
#             "help": "❓ Kömək",
#             "admin": "⚙️ Admin panel"
#         }
#     }
    
#     builder = ReplyKeyboardBuilder()
#     builder.button(text=texts[language]["profile"])
#     builder.button(text=texts[language]["report"])
#     builder.button(text=texts[language]["help"])
#     if is_admin:
#         builder.button(text=texts[language]["admin"])
#     builder.adjust(2)  # 2 кнопки в строке
#     return builder.as_markup(resize_keyboard=True)


# def get_edit_profile_keyboard(language: str = "ru") -> InlineKeyboardMarkup:
#     """Клавиатура для редактирования профиля"""
#     texts = {
#         "ru": {
#             "first_name": "✏️ Изменить имя",
#             "last_name": "✏️ Изменить фамилию",
#             "work_time": "⏰ Изменить время работы",
#             "language": "🌐 Изменить язык",
#             "back": "◀️ Назад"
#         },
#         "az": {
#             "first_name": "✏️ Adı dəyişdir",
#             "last_name": "✏️ Soyadı dəyişdir",
#             "work_time": "⏰ İş vaxtını dəyişdir",
#             "language": "🌐 Dili dəyişdir",
#             "back": "◀️ Geri"
#         }
#     }
    
#     builder = InlineKeyboardBuilder()
#     builder.button(text=texts[language]["first_name"], callback_data="edit_first_name")
#     builder.button(text=texts[language]["last_name"], callback_data="edit_last_name")
#     builder.button(text=texts[language]["work_time"], callback_data="edit_work_time")
#     builder.button(text=texts[language]["language"], callback_data="edit_language")
#     builder.button(text=texts[language]["back"], callback_data="back_to_menu")
#     builder.adjust(1)
#     return builder.as_markup()


# def get_admin_keyboard(language: str = "ru") -> InlineKeyboardMarkup:
#     """Клавиатура для админ-панели"""
#     texts = {
#         "ru": {
#             "stats": "📊 Статистика",
#             "users": "👥 Пользователи",
#             "reports": "📋 Отчеты за сегодня",
#             "weekly": "📅 Недельный отчет"
#         },
#         "az": {
#             "stats": "📊 Statistika",
#             "users": "👥 İstifadəçilər",
#             "reports": "📋 Bugünkü hesabatlar",
#             "weekly": "📅 Həftəlik hesabat"
#         }
#     }
    
#     builder = InlineKeyboardBuilder()
#     builder.button(text=texts[language]["stats"], callback_data="admin_stats")
#     builder.button(text=texts[language]["users"], callback_data="admin_users")
#     builder.button(text=texts[language]["reports"], callback_data="admin_daily_reports")
#     builder.button(text=texts[language]["weekly"], callback_data="admin_weekly_report")
#     builder.adjust(2)  # 2 кнопки в строке
#     return builder.as_markup()

from aiogram.types import InlineKeyboardMarkup, ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

def get_language_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="🇦🇿 Azərbaycanca", callback_data="lang_az")
    builder.button(text="🇷🇺 Русский", callback_data="lang_ru")
    builder.adjust(1)
    return builder.as_markup()

def get_work_time_keyboard(language: str = "ru") -> InlineKeyboardMarkup:
    texts = {
        "ru": {"morning": "🌅 9:00 - 18:00", "afternoon": "🌆 10:00 - 19:00"},
        "az": {"morning": "🌅 9:00 - 18:00", "afternoon": "🌆 10:00 - 19:00"}
    }
    builder = InlineKeyboardBuilder()
    builder.button(text=texts[language]["morning"], callback_data="work_time_9-18")
    builder.button(text=texts[language]["afternoon"], callback_data="work_time_10-19")
    # кнопка «Назад» к фамилии
    back_txt = "◀️ Назад" if language == "ru" else "◀️ Geri"
    builder.button(text=back_txt, callback_data="back_to_last_name")
    builder.adjust(1)
    return builder.as_markup()

def get_confirmation_keyboard(language: str = "ru") -> InlineKeyboardMarkup:
    """
    На экране подтверждения — только Подтвердить / Изменить.
    Кнопку «Отменить» по твоему запросу убрал.
    """
    texts = {
        "ru": {"confirm": "✅ Подтвердить", "edit": "✏️ Изменить"},
        "az": {"confirm": "✅ Təsdiq et", "edit": "✏️ Dəyişdir"},
    }
    builder = InlineKeyboardBuilder()
    builder.button(text=texts[language]["confirm"], callback_data="confirm_yes")
    builder.button(text=texts[language]["edit"], callback_data="confirm_edit")
    builder.adjust(1)
    return builder.as_markup()

# «Отменить» оставляем для сценариев редактирования (профиль/отчет)
def get_cancel_keyboard(language: str = "ru") -> InlineKeyboardMarkup:
    texts = {"ru": "❌ Отменить", "az": "❌ Ləğv et"}
    builder = InlineKeyboardBuilder()
    builder.button(text=texts[language], callback_data="cancel")
    return builder.as_markup()

def get_report_type_keyboard(language: str = "ru") -> InlineKeyboardMarkup:
    texts = {
        "ru": {"has_tasks": "📝 Есть задачи для отчета", "no_tasks": "🚫 Задач не было"},
        "az": {"has_tasks": "📝 Hesabat üçün tapşırıqlar var", "no_tasks": "🚫 Tapşırıq olmayıb"},
    }
    builder = InlineKeyboardBuilder()
    builder.button(text=texts[language]["has_tasks"], callback_data="report_has_tasks")
    builder.button(text=texts[language]["no_tasks"], callback_data="report_no_tasks")
    builder.adjust(1)
    return builder.as_markup()

def get_main_menu_keyboard(language: str = "ru", is_admin: bool = False) -> ReplyKeyboardMarkup:
    texts = {
        "ru": {"profile": "👤 Мой профиль", "report": "📊 Отправить отчет", "help": "❓ Помощь", "admin": "⚙️ Админ-панель"},
        "az": {"profile": "👤 Mənim profilim", "report": "📊 Hesabat göndər", "help": "❓ Kömək", "admin": "⚙️ Admin panel"},
    }
    builder = ReplyKeyboardBuilder()
    builder.button(text=texts[language]["profile"])
    builder.button(text=texts[language]["report"])
    builder.button(text=texts[language]["help"])
    if is_admin:
        builder.button(text=texts[language]["admin"])
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)

def get_edit_profile_keyboard(language: str = "ru") -> InlineKeyboardMarkup:
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

# --- вспомогательные «Назад» для регистрации ---

def get_back_from_last_name_keyboard(language: str = "ru") -> InlineKeyboardMarkup:
    """Кнопка «Назад» с шага фамилии к имени"""
    txt = "◀️ Назад" if language == "ru" else "◀️ Geri"
    b = InlineKeyboardBuilder()
    b.button(text=txt, callback_data="back_to_first_name")
    return b.as_markup()

def get_back_from_work_time_keyboard(language: str = "ru") -> InlineKeyboardMarkup:
    """Кнопка «Назад» с шага времени к фамилии (не используется — мы встроили назад в саму клаву времени)"""
    txt = "◀️ Назад" if language == "ru" else "◀️ Geri"
    b = InlineKeyboardBuilder()
    b.button(text=txt, callback_data="back_to_last_name")
    return b.as_markup()
