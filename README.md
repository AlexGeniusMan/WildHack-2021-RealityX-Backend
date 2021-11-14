## 🧭 Contents:

* [🗒️ Description](#description)
* [➡️ Launching](#launching)
* [🧾 Documentation](#documentation)

<a name="description"></a>

## 🗒️ Description

This is core backend service for [WildHack](https://github.com/AlexGeniusMan/WildHack-2021-RealityX) project

<a name="launching"></a>

## ➡️ Launching

1. At first install:

- [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
- [Docker](https://docs.docker.com/get-docker/)
- [Python 3](https://www.python.org/downloads/)

2. Clone repo:

```
git clone https://github.com/AlexGeniusMan/WildHack-2021-RealityX-Backend wildhack-backend
cd wildhack-backend
```

3. Create .env file and add secrets to it:

```
BACKEND_DEBUG_MODE=True
BACKEND_SECRET_KEY=YOUR_BACKEND_SECRET_KEY
BACKEND_ALLOWED_HOSTS="127.0.0.1 localhost"

BACKEND_SUPERUSER_USERNAME=YOUR_BACKEND_SUPERUSER_USERNAME
BACKEND_SUPERUSER_EMAIL=YOUR_BACKEND_SUPERUSER_EMAIL
BACKEND_SUPERUSER_PASSWORD=YOUR_BACKEND_SUPERUSER_PASSWORD

BACKEND_DEFAULT_DB=PostgreSQL
```

> - To generate new BACKEND_SECRET_KEY use [this](https://stackoverflow.com/a/57678930/14355198) instruction
> - BACKEND_ALLOWED_HOSTS must be a list of allowed hosts, separated by whitespaces. To see how to configure it, look at [this](https://docs.djangoproject.com/en/3.2/ref/settings/#allowed-hosts) instruction

4. Launch with Docker Compose:

```
docker-compose -f docker-compose.override.yml up --build
```

> Done! Project launched.

<a name="documentation"></a>

## 🧾 Documentation

Documentation is available at:

- [https://www.wildhack.reality-x.space/api/swagger/](https://www.wildhack.reality-x.space/api/swagger/)

