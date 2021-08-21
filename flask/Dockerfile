FROM python:3.9.6-alpine3.13

RUN pip3 install --upgrade pip
RUN pip3 install wheel

COPY requirements.txt /
RUN pip3 install -r /requirements.txt

COPY . /app
WORKDIR /app

ENTRYPOINT ["./gunicorn.sh"]
