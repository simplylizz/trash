FROM python:3.7.0

RUN pip install --no-cache-dir -U pip
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir /host
WORKDIR /host
