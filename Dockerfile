FROM sleekybadger/libpostal:1.1-alpha-alpine as libpostal-build

FROM python:3.7-alpine
ENV PYTHONUNBUFFERED 1

# Libpostal stuff
COPY --from=libpostal-build /data /data
COPY --from=libpostal-build /usr/lib/libpostal.so /usr/lib/libpostal.so
COPY --from=libpostal-build /usr/lib/libpostal.so.1 /usr/lib/libpostal.so.1
COPY --from=libpostal-build /usr/include/libpostal /usr/include/libpostal

RUN apk add --no-cache build-base

RUN mkdir /code
# Download dependencies
WORKDIR /code
COPY Pipfile Pipfile
COPY Pipfile.lock Pipfile.lock
RUN pip install --upgrade pip && pip install pipenv && pipenv install

COPY . /code/


CMD pipenv run gunicorn main:app -w 5 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000 --preload
