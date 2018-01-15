FROM python:alpine3.6
ENV PYTHONUNBUFFERED 1
RUN mkdir /app/
WORKDIR /app/
ADD . /app/
RUN pip install -r requirements.txt
RUN python manage.py makemigrations
RUN python manage.py migrate