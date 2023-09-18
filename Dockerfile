FROM python:3



COPY requirements.txt /
RUN pip install -r requirements.txt

COPY command.py /

CMD python -u /command.py
