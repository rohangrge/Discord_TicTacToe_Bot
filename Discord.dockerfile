FROM python:3.8.0-buster


COPY requirements.txt .
RUN pip install -r requirements.txt


COPY . .
CMD ["python","bot.py"]