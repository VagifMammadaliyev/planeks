FROM python:3.9.5-buster

ENV PYTHONUNBUFFERED 1

WORKDIR /code

COPY Pipfile Pipfile
COPY Pipfile.lock Pipfile.lock

RUN pip install --upgrade pip \
    && pip install pipenv \
    && pipenv install --system --deploy --ignore-pipfile --clear

COPY uwsgi.ini uwsgi.ini

COPY ./app .

CMD ["uwsgi", "--ini", "uwsgi.ini"]
