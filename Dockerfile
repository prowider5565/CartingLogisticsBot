FROM python:3.11

ENV PYTHONUNBUFFERED 1

# Создание директории для приложения
RUN mkdir /navbatda-backend

COPY ./migration.sh /


# Обновление пакетов и установка необходимых утилит
RUN apt-get update && \
    apt-get install -y gcc gunicorn \
  && rm -rf /var/lib/apt/lists/*

# Установка рабочей директории
WORKDIR /navbatda-backend

# Копирование requirements.txt перед копированием всего проекта
COPY requirements.txt .

# Установка зависимостей
RUN pip install -r requirements.txt && apt update

# Удаление gcc
RUN apt-get purge -y \
  gcc \
  && rm -rf /var/lib/apt/lists/*

# Копирование остальной части приложения
COPY . .

RUN chmod 777 ./migration.sh

RUN mkdir -p /app/src/media && chmod -R 777 /app/src/media
#WORKDIR src

#CMD ["gunicorn", "src.runner:app", "--workers 4", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind=0.0.0.0:8001"]

ENTRYPOINT ["sh", "-c", "sh ./migration.sh"]
