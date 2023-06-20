FROM python:3.11.3

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY .env .env
COPY src src

WORKDIR /src
CMD ["python", "-u", "./bot.py"]