FROM python:3.7-slim-buster as base

COPY ./books/requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt

RUN mkdir -p /src
COPY books/ /src/books/

WORKDIR /src

FROM base as debug
# Debug image reusing the base
# Install dev dependencies for debugging
RUN pip install debugpy