FROM python:3

RUN pip install pika requests

COPY command.py /

CMD python -u /command.py
