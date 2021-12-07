FROM python:3.8-bullseye

RUN pip3 install pika requests validators && \
    apt-get update && apt-get -y install perl && \
    apt-get clean && rm -rf /var/lib/apt/lists/* && \
    mkdir -p /code && \
    mkdir -p /log
COPY src /src
COPY service /code/service
COPY test.py /code/test.py
WORKDIR /code