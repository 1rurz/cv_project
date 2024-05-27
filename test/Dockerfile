FROM python:3.12

LABEL authors="rurz"

RUN mkdir /app/test

COPY . /app/test

WORKDIR /app/test

CMD ["python", "test.py"]