FROM python:3.6.12-alpine

RUN pip3 install --upgrade pip

COPY requirements.txt /
RUN pip3 install -r /requirements.txt

COPY . /app
WORKDIR /app

ENTRYPOINT ["./run_bot.sh"]
