FROM python:alpine3.6
ENV PYTHONUNBUFFERED 1
RUN mkdir /app/
WORKDIR /app/
ADD . /app/
# RUN apk add --update curl gcc g++ \
#     && rm -rf /var/cache/apk/*
# RUN ln -s /usr/include/locale.h /usr/include/xlocale.h
# RUN pip install bottle numpy cython pandas
# CMD tail -f /dev/null
RUN pip install --no-cache-dir -r requirements.txt
RUN python manage.py migrate