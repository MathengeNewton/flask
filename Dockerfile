FROM  python:latest

WORKDIR /app

ADD . /app

RUN pip install -r requirments.txt

CMD 
