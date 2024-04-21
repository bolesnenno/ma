# Используем официальный образ Python
FROM python:3.9-slim

# Установка зависимостей для работы с PostgreSQL
RUN apt-get update && apt-get install -y libpq-dev gcc && rm -rf /var/lib/apt/lists/*

# Установка рабочей директории в контейнере
WORKDIR /app

# Копирование файлов requirements.txt и установка зависимостей Python
COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Копирование остальных файлов проекта
COPY . /app

# Объявление порта, на котором будет работать приложение
EXPOSE 8000

# Команда для запуска приложения
CMD ["flask", "run", "--host=0.0.0.0", "--port=80"]
