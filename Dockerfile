#FROM alpine:latest
#
#RUN apk add --no-cache python3-dev \
#  && pip3 install --upgrade pip
#
#RUN echo 'http://dl-cdn.alpinelinux.org/alpine/v3.6/main' >> /etc/apk/repositories
#RUN echo 'http://dl-cdn.alpinelinux.org/alpine/v3.6/community' >> /etc/apk/repositories
#RUN apk update
#RUN apk add mongodb=3.4.4-r0
#
#WORKDIR /app
#
#COPY . /app
#
#RUN pip3 --no-cache-dir install -r requirements.txt
#
#RUN mongod --bind_ip='0.0.0.0'
#
#EXPOSE 5000 27017
#
#ENTRYPOINT ["python3"]
#
#CMD ["src/app.py"]

FROM python:3.6

ADD . /app

WORKDIR /app

RUN pip install -r requirements.txt
