FROM python:3.7.0

RUN pip install --no-cache-dir -U pip
ADD requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY ./chemondis /app
WORKDIR /app

EXPOSE 8080

RUN python manage.py migrate --noinput

ENTRYPOINT ["python", "manage.py"]
CMD ["runserver", "0.0.0.0:8080"]
