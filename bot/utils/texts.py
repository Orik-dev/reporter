from typing import Dict

TEXTS: Dict[str, Dict[str, str]] = {
    "ru": {
        # Старт и регистрация
        "welcome": "👋 Добро пожаловать!\n\nВыберите язык:",
        "enter_first_name": "📝 Введите ваше имя:",
        "enter_last_name": "📝 Введите вашу фамилию:",
        "select_work_time": "⏰ Выберите ваше рабочее время:",
        "confirm_registration": (
            "📋 Подтвердите регистрацию:\n\n"
            "Имя: {first_name}\n"
            "Фамилия: {last_name}\n"
            "Время работы: {work_time}\n"
            "Язык: Русский"
        ),
        "registration_success": "✅ Регистрация успешно завершена!",

        # Профиль
        "profile_info": (
            "👤 Ваш профиль:\n\n"
            "Имя: {first_name}\n"
            "Фамилия: {last_name}\n"
            "Время работы: {work_time}\n"
            "Язык: Русский"
        ),
        "profile_updated": "✅ Профиль успешно обновлен!",

        # Отчеты
        "report_request": (
            "⏰ Рабочий день закончен!\n\n"
            "Пожалуйста, отправьте отчет о выполненных задачах за сегодня.\n"
            "Если задач не было, нажмите соответствующую кнопку."
        ),
        "report_type_select": "Выберите тип отчета:",
        "enter_report_text": "📝 Опишите задачи, которые вы выполнили сегодня:",
        "report_submitted": "✅ Отчет успешно отправлен!",
        "report_no_tasks": "✅ Отмечено, что задач не было",
        "report_already_submitted": "ℹ️ Вы уже отправили отчет за сегодня",

        # Напоминания
        "reminder": (
            "⏰ Напоминание!\n\n"
            "Вы еще не отправили отчет за сегодня.\n"
            "Пожалуйста, отправьте отчет о выполненных задачах."
        ),

        # Админ
        "admin_panel": "⚙️ Админ-панель\n\nВыберите действие:",
        "daily_report_summary": (
            "📊 Отчет за {date}\n\n"
            "Всего пользователей: {total}\n"
            "✅ Отправили отчет: {submitted}\n"
            "❌ Не отправили: {not_submitted}\n"
            "🚫 Без задач: {no_tasks}\n\n"
            "{details}"
        ),
        "user_list": "👥 Список пользователей ({count}):\n\n{users}",
        "stats": (
            "📊 Статистика:\n\n"
            "Всего пользователей: {total_users}\n"
            "Активных: {active_users}\n"
            "Отчетов за сегодня: {today_reports}\n"
            "Отчетов за неделю: {week_reports}"
        ),

        # Ошибки и общее
        "error": "❌ Произошла ошибка. Попробуйте еще раз.",
        "invalid_input": "❌ Некорректный ввод. Попробуйте еще раз.",
        "invalid_name": "❌ Некорректное имя. Допускаются только буквы, пробел, дефис, апостроф (2–50 символов).",
        "invalid_last_name": "❌ Некорректная фамилия. Допускаются только буквы, пробел, дефис, апостроф (2–50 символов).",
        "not_authorized": "❌ У вас нет доступа к этой функции",
        "help_text": (
            "❓ Помощь\n\n"
            "Этот бот помогает отслеживать ежедневные задачи сотрудников.\n\n"
            "Основные команды:\n"
            "/start - Начать работу с ботом\n"
            "/profile - Просмотр профиля\n"
            "/report - Отправить отчет\n"
            "/help - Показать это сообщение"
        ),
        "finish_registration_first": "ℹ️ Сначала завершите регистрацию, пожалуйста.",
    },
    "az": {
        "welcome": "👋 Xoş gəlmisiniz!\n\nDili seçin:",
        "enter_first_name": "📝 Adınızı daxil edin:",
        "enter_last_name": "📝 Soyadınızı daxil edin:",
        "select_work_time": "⏰ İş vaxtınızı seçin:",
        "confirm_registration": (
            "📋 Qeydiyyatı təsdiq edin:\n\n"
            "Ad: {first_name}\n"
            "Soyad: {last_name}\n"
            "İş vaxtı: {work_time}\n"
            "Dil: Azərbaycan"
        ),
        "registration_success": "✅ Qeydiyyat uğurla tamamlandı!",

        "profile_info": (
            "👤 Sizin profiliniz:\n\n"
            "Ad: {first_name}\n"
            "Soyad: {last_name}\n"
            "İş vaxtı: {work_time}\n"
            "Dil: Azərbaycan"
        ),
        "profile_updated": "✅ Profil uğurla yeniləndi!",

        "report_request": (
            "⏰ İş günü bitdi!\n\n"
            "Zəhmət olmasa, bu gün görülən işlər haqqında hesabat göndərin.\n"
            "Əgər tapşırıq olmayıbsa, müvafiq düyməni basın."
        ),
        "report_type_select": "Hesabat növünü seçin:",
        "enter_report_text": "📝 Bu gün yerinə yetirdiyiniz tapşırıqları təsvir edin:",
        "report_submitted": "✅ Hesabat uğurla göndərildi!",
        "report_no_tasks": "✅ Tapşırıq olmadığı qeyd edildi",
        "report_already_submitted": "ℹ️ Siz bu gün artıq hesabat göndərmisiniz",

        "reminder": (
            "⏰ Xatırlatma!\n\n"
            "Siz hələ bu gün üçün hesabat göndərməmisiniz.\n"
            "Zəhmət olmasa, görülən işlər haqqında hesabat göndərin."
        ),

        "admin_panel": "⚙️ Admin panel\n\nƏməliyyatı seçin:",
        "daily_report_summary": (
            "📊 {date} tarixli hesabat\n\n"
            "Cəmi istifadəçi: {total}\n"
            "✅ Hesabat göndərdi: {submitted}\n"
            "❌ Göndərmədi: {not_submitted}\n"
            "🚫 Tapşırıqsız: {no_tasks}\n\n"
            "{details}"
        ),
        "user_list": "👥 İstifadəçilər siyahısı ({count}):\n\n{users}",
        "stats": (
            "📊 Statistika:\n\n"
            "Cəmi istifadəçi: {total_users}\n"
            "Aktiv: {active_users}\n"
            "Bu günkü hesabatlar: {today_reports}\n"
            "Həftəlik hesabatlar: {week_reports}"
        ),

        "error": "❌ Xəta baş verdi. Yenidən cəhd edin.",
        "invalid_input": "❌ Yanlış məlumat. Yenidən cəhd edin.",
        "invalid_name": "❌ Yanlış ad. Yalnız hərflər, boşluq, tire, apostrof (2–50 simvol).",
        "invalid_last_name": "❌ Yanlış soyad. Yalnız hərflər, boşluq, tire, apostrof (2–50 simvol).",
        "not_authorized": "❌ Bu funksiyaya girişiniz yoxdur",
        "help_text": (
            "❓ Kömək\n\n"
            "Bu bot işçilərin gündəlik tapşırıqlarını izləməyə kömək edir.\n\n"
            "Əsas əmrlər:\n"
            "/start - Botla işə başla\n"
            "/profile - Profilə bax\n"
            "/report - Hesabat göndər\n"
            "/help - Bu mesajı göstər"
        ),
        "finish_registration_first": "ℹ️ Zəhmət olmasa, əvvəlcə qeydiyyatı tamamlayın.",
    }
}

def get_text(key: str, language: str = "ru", **kwargs) -> str:
    try:
        text = TEXTS[language][key]
        return text.format(**kwargs) if kwargs else text
    except KeyError:
        base = TEXTS["ru"].get(key, "Текст не найден")
        return base.format(**kwargs) if kwargs else base
