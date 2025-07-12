FROM python:3.11-slim

ENV VALID_COINS=[5,10,20,50,100]

WORKDIR /code

RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /code/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . /code/
CMD ["gunicorn", "backend.wsgi:application", "--bind", "0.0.0.0:8000"]