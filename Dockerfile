FROM python:3.10

WORKDIR /src

ENV PYTHONDONTWRITEBYTECODE true
ENV PYTHONUNBUFFERED true

RUN pip install --upgrade pip

COPY requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt

COPY src/ .
RUN pip install -e /src
