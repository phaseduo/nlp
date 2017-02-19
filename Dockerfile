FROM python:2.7.12
MAINTAINER Alastair Paragas "alastairparagas@gmail.com"

ADD requirements.txt requirements.txt

RUN pip install -r requirements.txt
RUN python -m spacy.en.download all

VOLUME /phaseduo_nlp
EXPOSE 8000
