FROM python:3.7-alpine
ENV PYTHONUNBUFFERED 1

RUN apk update && apk add --no-cache build-base jpeg-dev zlib-dev postgresql-dev g++ gcc python3-dev musl-dev bash tzdata mailcap; \
    cp /usr/share/zoneinfo/America/Sao_Paulo /etc/localtime; \
    echo "America/Sao_Paulo" > /etc/timezone

RUN mkdir /code
WORKDIR /code
COPY . /code
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r /code/requirements.txt
