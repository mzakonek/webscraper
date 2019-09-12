FROM python:3.7-alpine
MAINTAINER Mateusz

ENV PYTHONUNBUFFERED 1

COPY requirements.txt requirements.txt
# RUN pip install -r /requirements.txt
RUN \
 apk add --no-cache postgresql-libs && \
 apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
 python3 -m pip install -r requirements.txt --no-cache-dir && \
 apk --purge del .build-deps


COPY . .

EXPOSE 8000