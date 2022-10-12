FROM python:3.7.15-alpine

EXPOSE 5000

COPY requirements.txt /
RUN pip3 install -r /requirements.txt

COPY . /app
WORKDIR /app

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]