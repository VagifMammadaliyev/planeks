# Planeks

A showcase task. Just helping someone else to apply for the job...

## Local development

### Start containers

```sh
docker-compose up -d
```

Note: **On production environment you need to run with `-f` flag due to how `docker-compose` command works**:

```sh
docker-compose -f docker-compose.yml -d
```

Although this is not needed as we are deploying to Heroku.

### Set up python environment

To set up a python environment for development we need to upgrade our pip installation
and install `pipenv` for our dependency management. [Read more](https://pypi.org/project/pipenv/)

```sh
pip install --upgrade pip && pip install pipenv
```

Now just install all dependencies from a lock file.

```sh
cd /path/to/project/folder/planeks && pipenv install
```

Last command will initialize virtual environment and install all necessary python packages.
To install packages necessary for development run `pipenv install --dev`.

### Run tests

Tests are written for core functionality only (like in most agile-developed projects).
To run tests we need to "up" `postgres` and `redis` containers

```sh
docker-compose up -d postgres redis && sleep 10 && python manage.py test -v 2
```

Note: _We are sleeping because we want to let postgres and redis start_
