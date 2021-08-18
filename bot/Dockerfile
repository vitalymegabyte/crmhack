FROM python:3.6.12-alpine

RUN sudo apt-get install libxml2-dev libxmlsec1-dev
RUN pip3 install --upgrade pip

COPY requirements.txt /
RUN pip3 install -r /requirements.txt

COPY . /app
WORKDIR /app

ENTRYPOINT ["./run_bot.sh"]
