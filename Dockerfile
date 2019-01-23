FROM python:3.7.2-alpine3.8
RUN apk add --no-cache --virtual build-dependencies git build-base python3-dev libffi-dev openssl-dev \
 && pip install --upgrade pip && pip install --upgrade cryptography cffi \
 && apk del build-dependencies

COPY requirements.txt /app/


RUN apk add --no-cache --virtual build-dependencies git \
 && pip install -r /app/requirements.txt \
 && apk del build-dependencies

COPY *.py /app/

ENTRYPOINT ["python", "/app/main.py"]