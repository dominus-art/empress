FROM python:3.11-alpine

WORKDIR /code

RUN apk update && apk upgrade

RUN apk --no-cache add cargo g++

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

CMD ["python3", "-OO", "main.py"]