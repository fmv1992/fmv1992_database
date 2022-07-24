# `analytics_database_schemas:4ae6c00:dockerfile:1`:

# ———————————————————————————————————————————————————————————————————————————————
# From:

# 1.    <https://██████.slack.com/archives/C03PND6MK7C/p1657886305657099>.
# 2.    <https://██████.slack.com/archives/C5WNXK932/p1658151502200749>.
FROM registry.internal.██████.com/library/library/ubuntu@sha256:9101220a875cee98b016668342c489ff0674f247f6ca20dfc91b91c0f28581ae

LABEL maintainer="██████ Engineering <engineering@██████.com>"

SHELL ["/bin/bash", "-euo", "pipefail", "-c"]

RUN apt-get update
RUN apt-get install --no-install-recommends --yes \
        ca-certificates \
        curl \
        gcc \
        gnupg2 \
        libpq-dev \
        lsb-release \
        make \
        parallel \
        python3-dev \
        python3-pip \
        vim

# Install `PostgreSQL`.
RUN command -V lsb_release
# As of 2022-04-11 `domo_warehouse` version is: `PostgreSQL 11.14`.
# As of 2022-04-11 `domo_dev_warehouse` version is: `PostgreSQL 11.14`.
RUN curl --location --output - -- https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add -
RUN echo "deb http://apt.postgresql.org/pub/repos/apt/ `lsb_release -cs`-pgdg main" | tee /etc/apt/sources.list.d/pgdg.list
RUN apt-get update && apt-get install --yes postgresql-client-11
RUN command -V psql && psql --version

# Install python libraries.
COPY ./requirements.txt /tmp/requirements.txt
RUN python3 -m pip install --requirement /tmp/requirements.txt
RUN rm /tmp/requirements.txt

RUN apt-get autoremove -yqq --purge \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set up unprivileged user.
# <https://docs.docker.com/develop/develop-images/dockerfile_best-practices/#user>.
# Also in `analytics-scripts:d76b146:dockerfile:26`.
ARG uid
ARG gid
ARG project
RUN groupadd --system --gid $gid ubuntu && useradd --no-log-init --create-home --system --gid ubuntu --uid $uid ubuntu
USER ubuntu
ENV HOME /home/ubuntu
ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8
WORKDIR "${HOME}/${project}"

ENV PYTHONPATH="${HOME}"

CMD []
ENTRYPOINT []
# ———————————————————————————————————————————————————————————————————————————————
