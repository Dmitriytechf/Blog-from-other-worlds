FROM python:3.12-slim

# Запрещаем создание .pyc файлов
ENV PYTHONDONTWRITEBYTECODE 1
# Отключаем буферизацию вывода Python
ENV PYTHONUNBUFFERED 1

# Создание и переход в рабочую директорию
WORKDIR /app

COPY requirements.txt .

RUN python -m pip install --upgrade pip --no-warn-script-location

RUN pip install -r requirements.txt --no-cache-dir --no-warn-script-location

COPY . .

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
