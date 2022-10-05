FROM python:3.9-buster
COPY . /app

RUN pip3 install -r requirements.txt
CMD python3 bot.py & python3 server.py