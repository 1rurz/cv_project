FROM python:3.11-alpine

LABEL authors="rurz"

RUN mkdir /app

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r docker build -t myjenkins-blueocean:2.452.1-1 .requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]

