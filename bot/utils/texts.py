"""
Тексты сообщений - ФИНАЛЬНАЯ ВЕРСИЯ
"""
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
        "report_too_early": (
            "⏰ Еще рано!\n\n"
            "Отчет можно отправить после {end_time}\n"
            "Рабочий день еще не закончился."
        ),

        # Напоминания
        "reminder": (
            "⏰ Напоминание!\n\n"
            "Вы еще не отправили отчет за сегодня.\n"
            "Пожалуйста, отправьте отчет о выполненных задачах."
        ),

        # Админ
        "admin_panel": "⚙️ Админ-панель\n\nВыберите действие:",
        "weekly_report_header": "📊 Еженедельный отчет\n📅 {week_start} - {week_end}",
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

        # Удаление пользователей
        "cannot_delete_self": "❌ Вы не можете удалить самого себя",
        "cannot_delete_admin": "❌ Нельзя удалить администратора",
        "user_not_found": "❌ Пользователь не найден",
        "delete_user_confirm": (
            "⚠️ Вы уверены, что хотите удалить пользователя?\n\n"
            "👤 {first_name} {last_name}\n\n"
            "❗️ Будут удалены:\n"
            "• Профиль пользователя\n"
            "• Все его отчеты\n\n"
            "Это действие необратимо!"
        ),
        "user_deleted": (
            "✅ Пользователь удален\n\n"
            "👤 {first_name} {last_name}\n\n"
            "Все данные пользователя удалены из системы."
        ),

        # Примеры отчетов
        "examples_header": "📝 Примеры отчетов\n\nВыберите вашу специальность:",
        "example_uiux": (
            "🎨 UI/UX Дизайнер:\n\n"
            "✅ Создал прототип главной страницы\n"
            "✅ Доработал дизайн-систему (цвета, шрифты)\n"
            "✅ Провел A/B тестирование кнопок CTA\n"
            "✅ Согласовал макеты с заказчиком"
        ),
        "example_graphic": (
            "🖼 Графический дизайнер:\n\n"
            "✅ Разработал 5 баннеров для соцсетей\n"
            "✅ Создал логотип для нового проекта\n"
            "✅ Подготовил презентацию (20 слайдов)\n"
            "✅ Отредактировал фото для сайта"
        ),
        "example_backend": (
            "⚙️ PHP Backend разработчик:\n\n"
            "✅ Исправил баг в модуле авторизации\n"
            "✅ Оптимизировал SQL запросы (ускорение на 40%)\n"
            "✅ Добавил API endpoint для отчетов\n"
            "✅ Провел code review для коллеги"
        ),
        "example_flutter": (
            "📱 Flutter разработчик:\n\n"
            "✅ Реализовал экран профиля пользователя\n"
            "✅ Интегрировал Firebase Authentication\n"
            "✅ Исправил краши на Android 12\n"
            "✅ Добавил push-уведомления"
        ),
        "example_seo": (
            "🔍 SEO специалист:\n\n"
            "✅ Провел аудит сайта (выявлено 15 проблем)\n"
            "✅ Оптимизировал 10 страниц под ключевые слова\n"
            "✅ Настроил Google Search Console\n"
            "✅ Проанализировал конкурентов (топ-5)"
        ),

        # Ошибки
        "error": "❌ Произошла ошибка. Попробуйте еще раз.",
        "invalid_input": "❌ Некорректный ввод. Попробуйте еще раз.",
        "invalid_name": (
            "❌ Некорректное имя.\n\n"
            "Допускаются только буквы, пробелы, дефисы, апострофы (2-50 символов).\n"
            "Пример: Иван, Мария-Анна, O'Connor"
        ),
        "invalid_last_name": (
            "❌ Некорректная фамилия.\n\n"
            "Допускаются только буквы, пробелы, дефисы, апострофы (2-50 символов).\n"
            "Пример: Иванов, Салтыков-Щедрин, O'Brien"
        ),
        "report_cancelled": "❌ Отправка отчета отменена",
        "report_too_short": "❌ Отчет слишком короткий. Минимум 10 символов.",
        "report_empty": "❌ Отчет не может быть пустым или состоять только из пробелов.",
        "not_authorized": "❌ У вас нет доступа к этой функции",
        "finish_registration_first": "ℹ️ Сначала завершите регистрацию, пожалуйста.",
        
        "help_text": (
            "❓ Помощь\n\n"
            "Этот бот помогает отслеживать ежедневные задачи сотрудников.\n\n"
            "Основные команды:\n"
            "/profile - Просмотр профиля\n"
            "/report - Отправить отчет\n"
            "/help - Показать это сообщение"
        ),
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
        "report_too_early": (
            "⏰ Hələ tezdir!\n\n"
            "Hesabatı {end_time}-dən sonra göndərə bilərsiniz\n"
            "İş günü hələ bitməyib."
        ),

        "reminder": (
            "⏰ Xatırlatma!\n\n"
            "Siz hələ bu gün üçün hesabat göndərməmisiniz.\n"
            "Zəhmət olmasa, görülən işlər haqqında hesabat göndərin."
        ),

        "admin_panel": "⚙️ Admin panel\n\nƏməliyyatı seçin:",
        "weekly_report_header": "📊 Həftəlik Hesabat\n📅 {week_start} - {week_end}",
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

        # Удаление пользователей
        "cannot_delete_self": "❌ Siz özünüzü silə bilməzsiniz",
        "cannot_delete_admin": "❌ Administratoru silmək olmaz",
        "user_not_found": "❌ İstifadəçi tapılmadı",
        "delete_user_confirm": (
            "⚠️ İstifadəçini silmək istədiyinizə əminsiniz?\n\n"
            "👤 {first_name} {last_name}\n\n"
            "❗️ Silinəcək:\n"
            "• İstifadəçi profili\n"
            "• Bütün hesabatları\n\n"
            "Bu əməliyyatı geri qaytarmaq mümkün deyil!"
        ),
        "user_deleted": (
            "✅ İstifadəçi silindi\n\n"
            "👤 {first_name} {last_name}\n\n"
            "İstifadəçinin bütün məlumatları sistemdən silindi."
        ),

        # Примеры отчетов
        "examples_header": "📝 Hesabat nümunələri\n\nİxtisasınızı seçin:",
        "example_uiux": (
            "🎨 UI/UX Dizayner:\n\n"
            "✅ Ana səhifənin prototipini yaratdım\n"
            "✅ Dizayn sistemini təkmilləşdirdim (rənglər, şriftlər)\n"
            "✅ CTA düymələri üçün A/B test apardım\n"
            "✅ Maketi müştəri ilə razılaşdırdım"
        ),
        "example_graphic": (
            "🖼 Qrafik dizayner:\n\n"
            "✅ Sosial şəbəkələr üçün 5 banner hazırladım\n"
            "✅ Yeni layihə üçün loqotip yaratdım\n"
            "✅ Təqdimat hazırladım (20 slayd)\n"
            "✅ Sayt üçün fotoları redaktə etdim"
        ),
        "example_backend": (
            "⚙️ PHP Backend developer:\n\n"
            "✅ Avtorizasiya modulunda bağı düzəltdim\n"
            "✅ SQL sorğularını optimallaşdırdım (40% sürətlənmə)\n"
            "✅ Hesabatlar üçün API endpoint əlavə etdim\n"
            "✅ Həmkarım üçün code review apardım"
        ),
        "example_flutter": (
            "📱 Flutter developer:\n\n"
            "✅ İstifadəçi profili ekranını reallaşdırdım\n"
            "✅ Firebase Authentication inteqrasiya etdim\n"
            "✅ Android 12-də crashları düzəltdim\n"
            "✅ Push bildirişlər əlavə etdim"
        ),
        "example_seo": (
            "🔍 SEO mütəxəssis:\n\n"
            "✅ Sayt auditini apardım (15 problem aşkarlandı)\n"
            "✅ 10 səhifəni açar sözlərə görə optimallaşdırdım\n"
            "✅ Google Search Console quraşdırdım\n"
            "✅ Rəqibləri təhlil etdim (top-5)"
        ),

        "error": "❌ Xəta baş verdi. Yenidən cəhd edin.",
        "invalid_input": "❌ Yanlış məlumat. Yenidən cəhd edin.",
        "invalid_name": (
            "❌ Yanlış ad.\n\n"
            "Yalnız hərflər, boşluq, tire, apostrof (2-50 simvol).\n"
            "Nümunə: Orxan, Məryəm-Anna"
        ),
        "invalid_last_name": (
            "❌ Yanlış soyad.\n\n"
            "Yalnız hərflər, boşluq, tire, apostrof (2-50 simvol).\n"
            "Nümunə: Əliyev, Hacı-Məmmədov"
        ),
        "report_cancelled": "❌ Hesabat göndərilməsi ləğv edildi",
        "report_too_short": "❌ Hesabat çox qısadır. Minimum 10 simvol.",
        "report_empty": "❌ Hesabat boş ola bilməz və ya yalnız boşluqlardan ibarət ola bilməz.",
        "not_authorized": "❌ Bu funksiyaya girişiniz yoxdur",
        "finish_registration_first": "ℹ️ Zəhmət olmasa, əvvəlcə qeydiyyatı tamamlayın.",
        
        "help_text": (
            "❓ Kömək\n\n"
            "Bu bot işçilərin gündəlik tapşırıqlarını izləməyə kömək edir.\n\n"
            "Əsas əmrlər:\n"
            "/start - Botla işə başla\n"
            "/profile - Profilə bax\n"
            "/report - Hesabat göndər\n"
            "/help - Bu mesajı göstər"
        ),
    }
}


def get_text(key: str, language: str = "ru", **kwargs) -> str:
    """Получить текст сообщения"""
    try:
        text = TEXTS[language][key]
        return text.format(**kwargs) if kwargs else text
    except KeyError:
        base = TEXTS["ru"].get(key, "Текст не найден")
        return base.format(**kwargs) if kwargs else base