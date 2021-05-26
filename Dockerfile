# Copyright (c) Datalayer, Inc https://datalayer.io
# Distributed under the terms of the MIT License.

FROM ubuntu:18.04

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y \
        curl git gcc g++ make sudo \
        python python3-pip \
        libpq-dev \
        postgresql postgresql-client postgresql-contrib && \
    rm -rf /var/lib/apt/lists/*

RUN curl -sL https://deb.nodesource.com/setup_14.x | bash - && \
    apt install nodejs

RUN npm install --global yarn

RUN useradd -ms /bin/bash datalayer

USER postgres

RUN echo "host all  all    0.0.0.0/0  md5" >> /etc/postgresql/10/main/pg_hba.conf

RUN echo "listen_addresses='*'" >> /etc/postgresql/10/main/postgresql.conf

RUN /etc/init.d/postgresql start && \
    psql -c "CREATE USER datalayer WITH SUPERUSER PASSWORD 'datalayer';" && \
    psql -c "CREATE DATABASE crossplane_examples;" && \
    psql -c "GRANT ALL PRIVILEGES ON DATABASE crossplane_examples TO datalayer;"

RUN /etc/init.d/postgresql start && \
    psql -c "CREATE TABLE USERS (ID SERIAL, FIRST_NAME TEXT NOT NULL, LAST_NAME TEXT NOT NULL);" -d crossplane_examples

USER root

RUN mkdir /opt/crossplane-examples
WORKDIR /opt/crossplane-examples

COPY . /opt/crossplane-examples/

RUN pip3 install -e .

RUN yarn && yarn build:prod

RUN sed -i "s|http://localhost:8765|.|g" dist/index.html

EXPOSE 8765

COPY entry-point.sh /usr/local/bin/entry-point.sh

CMD ["/usr/local/bin/entry-point.sh"]
