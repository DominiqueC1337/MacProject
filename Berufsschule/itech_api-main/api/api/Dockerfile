FROM python:alpine3.16

VOLUME ["/app/shared"]

WORKDIR /app

RUN addgroup -S fastapi \
    && adduser -S fastapi -G fastapi \
    && apk update \
    && apk add --virtual build-deps \
      build-base \
      gcc \
      python3-dev \
      musl-dev \
      libffi-dev \
    && apk add --no-cache \
      mariadb-dev

USER fastapi
COPY requirements.txt /app/
RUN pip install -r requirements.txt

USER root
RUN apk del build-deps

USER fastapi
COPY ./config/ /app
COPY ./src/ /app

EXPOSE 8080
CMD [ "python", "main.py" ]
