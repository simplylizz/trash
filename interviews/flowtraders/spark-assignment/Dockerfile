FROM python:3.8.5-alpine3.12

RUN pip install --no-cache-dir \
        pyspark==3.0.0 \
        ipython==7.18.0 \
        pyreadline==2.1 \
        pytest==6.0.1 \
        ipdb==0.13.3 && \
    apk add --no-cache \
        openjdk11-jre \
        bash
