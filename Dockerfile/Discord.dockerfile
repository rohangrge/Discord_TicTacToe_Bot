FROM python:3.8.0-buster

WORKDIR /

COPY requirements.txt
RUN pip install -r requirements.txt

COPY /

CMD ["python","main.py"]