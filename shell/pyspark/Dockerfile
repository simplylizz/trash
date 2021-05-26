FROM python:3.9.5-alpine

# no pinned versions for interview ¯\_(ツ)_/¯
RUN pip install --no-cache-dir \
        pyspark \
        ipython \
        pyreadline \
        pytest \
        ipdb && \
    apk add --no-cache \
        openjdk11-jre \
        bash \
        less \
        vim \
        curl \
        wget
RUN wget https://jdbc.postgresql.org/download/postgresql-42.2.20.jar \
    -O /opt/postgresql.jar

