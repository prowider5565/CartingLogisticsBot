FROM python:3.11

ENV PYTHONUNBUFFERED 1
RUN mkdir /carting_bot
WORKDIR /carting_bot
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
RUN chmod 777 ./launcher.sh
RUN mkdir -p /app/media && chmod -R 777 /app/media
ENTRYPOINT ["sh", "-c", "sh ./launcher.sh"]
