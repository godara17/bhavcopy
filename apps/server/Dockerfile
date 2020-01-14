FROM ubuntu:18.04

ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install apt-utils -y

RUN apt-get update && apt-get install systemd -y

RUN apt-get update && apt-get install -y zip \
    unzip \
    vim \
    curl \
    wget \
    libicu-dev \
    nano


# COPY files which are needed
COPY installation.sh .

RUN /bin/sh installation.sh

COPY requirements.txt .

RUN apt-get update && pip3 install -r requirements.txt

COPY ./app /app

WORKDIR /app

EXPOSE 2729

# Run launch.sh when the container launches
CMD ["/bin/sh", "launch.sh"]
