FROM python:3.7-slim-buster as base

COPY ./ratings/requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt

RUN mkdir -p /src
WORKDIR /src
# COPY books/ /src/books/

FROM base as debug
# Debug image reusing the base
# Install dev dependencies for debugging
RUN pip install debugpy