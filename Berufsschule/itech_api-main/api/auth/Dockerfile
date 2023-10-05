FROM python:alpine3.16

WORKDIR /app

RUN addgroup -S itech.aapi \
    && adduser -S itech.aapi -G itech.aapi \
    && apk update \
    && apk add --virtual build-deps \
      build-base \
      gcc \
      python3-dev \
      musl-dev \
      libffi-dev \
      jpeg-dev \
      zlib-dev \
    && apk add --no-cache \
      mariadb-dev

USER itech.aapi
COPY requirements.txt /app/
RUN pip install -r requirements.txt

USER root
RUN apk del build-deps

USER itech.aapi
COPY ./config/ /app
COPY ./src/ /app

VOLUME ["/app/shared"]
EXPOSE 8080
CMD [ "python", "main.py" ]
