FROM python:3.7-slim
RUN python3 -m pip install --upgrade pip
#RUN apk add --no-cache --update \
#    python3 python3-dev gcc \
#    gfortran linux-headers  musl-dev g++ \
#    libffi-dev openssl-dev \
#    libxml2 libxml2-dev \
#    libxslt libxslt-dev \
#    libjpeg-turbo-dev zlib-dev libc-dev

COPY requirements.txt /
#RUN apk -y update && apk add python3-dev gcc libc-dev
RUN pip3 install -r requirements.txt
COPY . .
WORKDIR /
CMD gunicorn --chdir . wsgi:application -w 1 --threads 1 -b 0.0.0.0:5000
