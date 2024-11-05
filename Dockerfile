FROM python:3.12 AS base
ENV PYTHONUNBUFFERED 1

ARG SECRET_KEY

WORKDIR /usr/src/scai-api

COPY . /usr/src/scai-api
COPY ./requirements.txt /usr/src/scai-api
RUN pip install -r requirements.txt
COPY ./entrypoint.sh /usr/src/scai-api

RUN chmod +x ./entrypoint.sh

EXPOSE 8000