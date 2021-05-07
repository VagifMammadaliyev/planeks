# Planeks

A showcase task. Just helping someone else to apply for the job...

## Local development

Start containers:

```sh
docker-compose up -d  # this will start everything except Django related containers
```

Note: **On production environment you need to run with `-f` flag due to how `docker-compose` command works**:

```sh
docker-compose -f docker-compose.yml -d
```
