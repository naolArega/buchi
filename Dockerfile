FROM python:3.9.10

WORKDIR /app

ADD requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt

EXPOSE 8000

COPY . /app

CMD ["gunicorn"]