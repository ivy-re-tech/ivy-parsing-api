FROM python:3.7

ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
COPY . /code/

RUN pip install --upgrade pip && pip install pipenv && pipenv install

CMD pipenv run gunicorn main:app -w 3 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000