FROM python:3.11-slim

WORKDIR /app

COPY echo_bot.py .

RUN pip install python-telegram-bot==20.7

CMD ["python", "echo_bot.py"]
