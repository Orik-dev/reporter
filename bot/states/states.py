"""
FSM (Finite State Machine) состояния для бота
"""
from aiogram.fsm.state import State, StatesGroup


class RegistrationStates(StatesGroup):
    """Состояния для процесса регистрации пользователя"""
    language = State()  # Выбор языка
    first_name = State()  # Ввод имени
    last_name = State()  # Ввод фамилии
    work_time = State()  # Выбор рабочего времени
    confirmation = State()  # Подтверждение данных


class ReportStates(StatesGroup):
    """Состояния для отправки ежедневного отчета"""
    waiting_for_report = State()  # Ожидание отчета
    confirm_no_tasks = State()  # Подтверждение отсутствия задач


class EditProfileStates(StatesGroup):
    """Состояния для редактирования профиля"""
    select_field = State()  # Выбор поля для редактирования
    edit_first_name = State()  # Редактирование имени
    edit_last_name = State()  # Редактирование фамилии
    edit_work_time = State()  # Редактирование рабочего времени
    edit_language = State()  # Редактирование языка