FROM tiangolo/uwsgi-nginx:python3.7

RUN apt update && apt -y install unixodbc-dev

ENV UWSGI_CHEAPER 4
ENV UWSGI_PROCESSES 64

ENV UWSGI_INI /ad_preview/uwsgi.ini

COPY ./ad_preview /ad_preview

WORKDIR /ad_preview
RUN pip install --upgrade pip && pip3 install -r requirements.txt