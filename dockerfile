FROM python:3.11

RUN mkdir /referall_app

WORKDIR /referall_app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

WORKDIR /referall_app/src