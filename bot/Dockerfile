FROM python:3.9.6-alpine3.13

RUN pip3 install --upgrade pip

COPY requirements.txt /
RUN pip3 install -r /requirements.txt

COPY . /app
WORKDIR /app

ENTRYPOINT ["./run_bot.sh"]
