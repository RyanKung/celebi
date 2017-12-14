FROM python:3.6-alpine

COPY Docker/pip.conf /etc/pip.conf
RUN mkdir /root/.pip
COPY Docker/pip.conf /root/pip.conf
ADD . /code
WORKDIR /code

RUN sed -i 'http://mirrors.ustc.edu.cn/alpine/v3.3/main/' /etc/apk/repositories
RUN apk add --update gcc musl-dev
RUN pip install -r requirements.txt
CMD ["make", "celebi"]
