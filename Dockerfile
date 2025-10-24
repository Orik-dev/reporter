FROM python:3.11-slim

# Не писать .pyc, немедленный вывод логов и явный PYTHONPATH
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

WORKDIR /app

# Системные утилиты (минимум). build-essential пригодится для некоторых колёс.
RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential \
    && rm -rf /var/lib/apt/lists/*

# Сначала зависимости – кешируется лучше
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Затем исходники
COPY . /app

# Запуск
CMD ["python", "main.py"]
