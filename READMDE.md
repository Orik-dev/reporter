-- ===================================
-- СКРИПТ СОЗДАНИЯ ТАБЛИЦ ДЛЯ БОТА
-- MySQL 5.7
-- ===================================

-- Удаляем существующие таблицы если нужно начать заново (ОСТОРОЖНО!)
-- DROP TABLE IF EXISTS `weekly_reports`;
-- DROP TABLE IF EXISTS `daily_reports`;
-- DROP TABLE IF EXISTS `users`;

-- ===================================
-- ТАБЛИЦА ПОЛЬЗОВАТЕЛЕЙ
-- ===================================
CREATE TABLE IF NOT EXISTS `users` (
  `id` INT NOT NULL AUTO_INCREMENT COMMENT 'Уникальный ID пользователя',
  `telegram_id` BIGINT NOT NULL COMMENT 'Telegram ID пользователя',
  `first_name` VARCHAR(255) NOT NULL COMMENT 'Имя пользователя',
  `last_name` VARCHAR(255) NOT NULL COMMENT 'Фамилия пользователя',
  `language` VARCHAR(2) NOT NULL COMMENT 'Язык интерфейса (ru/az)',
  `work_time` VARCHAR(20) NOT NULL COMMENT 'Рабочее время (9:00-18:00 или 10:00-19:00)',
  `is_active` TINYINT(1) NOT NULL DEFAULT 1 COMMENT 'Активен ли пользователь',
  `is_admin` TINYINT(1) NOT NULL DEFAULT 0 COMMENT 'Является ли администратором',
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Дата создания',
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT 'Дата обновления',
  PRIMARY KEY (`id`),
  UNIQUE KEY `telegram_id` (`telegram_id`),
  KEY `idx_telegram_id` (`telegram_id`),
  KEY `idx_is_active` (`is_active`),
  KEY `idx_work_time` (`work_time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Таблица пользователей бота';

-- ===================================
-- ТАБЛИЦА ЕЖЕДНЕВНЫХ ОТЧЕТОВ
-- ===================================
CREATE TABLE IF NOT EXISTS `daily_reports` (
  `id` INT NOT NULL AUTO_INCREMENT COMMENT 'Уникальный ID отчета',
  `user_id` INT NOT NULL COMMENT 'ID пользователя (внешний ключ)',
  `telegram_id` BIGINT NOT NULL COMMENT 'Telegram ID пользователя (для быстрого поиска)',
  `report_date` DATETIME NOT NULL COMMENT 'Дата отчета',
  `report_text` TEXT DEFAULT NULL COMMENT 'Текст отчета (NULL если задач не было)',
  `has_tasks` TINYINT(1) NOT NULL COMMENT 'Были ли задачи (1-да, 0-нет)',
  `submitted_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Дата отправки отчета',
  `reminder_count` INT NOT NULL DEFAULT 0 COMMENT 'Количество отправленных напоминаний',
  PRIMARY KEY (`id`),
  KEY `idx_user_id` (`user_id`),
  KEY `idx_telegram_id` (`telegram_id`),
  KEY `idx_report_date` (`report_date`),
  KEY `idx_submitted_at` (`submitted_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Таблица ежедневных отчетов';

-- ===================================
-- ТАБЛИЦА НЕДЕЛЬНЫХ ОТЧЕТОВ
-- ===================================
CREATE TABLE IF NOT EXISTS `weekly_reports` (
  `id` INT NOT NULL AUTO_INCREMENT COMMENT 'Уникальный ID отчета',
  `week_start` DATETIME NOT NULL COMMENT 'Дата начала недели',
  `week_end` DATETIME NOT NULL COMMENT 'Дата окончания недели',
  `report_text` TEXT NOT NULL COMMENT 'Текст отчета (сгенерирован AI)',
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Дата создания',
  PRIMARY KEY (`id`),
  KEY `idx_week_start` (`week_start`),
  KEY `idx_created_at` (`created_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Таблица недельных отчетов';

-- ===================================
-- ПРОВЕРКА СОЗДАННЫХ ТАБЛИЦ
-- ===================================
SHOW TABLES;

-- ===================================
-- ПРОСМОТР СТРУКТУРЫ ТАБЛИЦ
-- ===================================
DESCRIBE users;
DESCRIBE daily_reports;
DESCRIBE weekly_reports;

-- ===================================
-- ГОТОВО!
-- ===================================
SELECT 'Таблицы успешно созданы!' AS status;
```

---

## 📋 **Инструкция по запуску (ПОШАГОВО):**

### **Шаг 1: Создание бота в Telegram**

1. Откройте Telegram и найдите [@BotFather](https://t.me/botfather)
2. Отправьте команду `/newbot`
3. Введите имя бота (например: "Daily Report Bot")
4. Введите username бота (например: "my_daily_report_bot")
5. **Скопируйте полученный токен** (выглядит так: `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz`)

### **Шаг 2: Получение вашего Telegram ID**

1. Найдите в Telegram бота [@userinfobot](https://t.me/userinfobot)
2. Отправьте ему `/start`
3. **Скопируйте ваш ID** (число, например: `123456789`)

### **Шаг 3: Создание таблиц в phpMyAdmin**

1. Откройте phpMyAdmin
2. Выберите базу данных `u2969681_emin`
3. Перейдите на вкладку **SQL**
4. **Скопируйте и вставьте весь SQL скрипт** (который я дал выше)
5. Нажмите **"Выполнить"**
6. Должно появиться сообщение "Таблицы успешно созданы!"

### **Шаг 4: Настройка файлов**

1. Создайте папку проекта (например: `telegram_bot`)
2. Создайте файл `.env` в корне проекта
3. **Скопируйте содержимое .env** (которое я дал выше)
4. **Замените** в `.env`:
   - `BOT_TOKEN=` на ваш токен от BotFather
   - `ADMIN_IDS=` на ваш Telegram ID

### **Шаг 5: Создание структуры папок**

Создайте следующую структуру:
```
telegram_bot/
├── .env
├── main.py
├── requirements.txt
├── config/
│   ├── __init__.py
│   └── settings.py
├── bot/
│   ├── __init__.py
│   ├── database/
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── connection.py
│   │   └── repository.py
│   ├── handlers/
│   │   ├── __init__.py
│   │   ├── start.py
│   │   ├── reports.py
│   │   ├── profile.py
│   │   ├── admin.py
│   │   └── common.py
│   ├── keyboards/
│   │   ├── __init__.py
│   │   └── keyboards.py
│   ├── middlewares/
│   │   ├── __init__.py
│   │   └── middlewares.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── deepseek_service.py
│   │   ├── document_service.py
│   │   └── scheduler_service.py
│   ├── states/
│   │   ├── __init__.py
│   │   └── states.py
│   ├── filters/
│   │   ├── __init__.py
│   │   └── filters.py
│   └── utils/
│       ├── __init__.py
│       └── texts.py
└── logs/ (создастся автоматически)