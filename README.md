# Workshops API

This is the API for a web app to manage workshop registrations.

I am using Flask with Flask-RESTful as framework, with Flask-SQLAlchemy for database.
Other libraries are PyJWT for auth tokens and Marshmallow for serialization.

It was made as a school project and I am not maintaining or supporting this.

*Note: The code is in English, but the UI is only in Dutch.*

## Features

- Let users register for workshops in an event
- Authenticate users with a unique login key for each user, either auto-generated or manually set
- Choose which groups of users can register for what
- Link workshops (e.g. A and B must be taken together, C and D can not be combined)
- Import/export users as CSV
- Export registrations as Excel with a worksheet for every workshop

## Installation guide

There are many ways to deploy this application. This method is the simplest.

This uses SQLite as your database so it does not scale to more than one node. If you are having performance issues, switch to a database server like MySQL, PostgreSQL or anything listed [here](https://docs.sqlalchemy.org/en/13/core/engines.html).

Things you need before you can start:

* Ubuntu Server 18.04 (other Linux distros should work as well)
* Docker on your server ([instructions for Ubuntu](https://docs.docker.com/install/linux/docker-ce/ubuntu/#install-using-the-repository))
* This repo

First, configure the application in `config.yml`. You should definitely change these options:

* `allowed_origin`: the URL for the web app
* `jwt_secret`: put some random string here

Build the docker image.

```
docker build -t workshops-api .
```

Create a volume to store the SQLite database in.

```
docker volume create workshops-db
```

Start the container and set it to always restart.

```
 docker run -d \
    --name workshops-api \
    --mount source=workshops-db,target=/data/db \
    -p 8000:8080 \
    --restart always \
    workshops-api
```

The API should be reachable at http://localhost:8000 now.

Next steps:

* Install the web frontend
* Put nginx or some other reverse proxy in front of it
* Set up HTTPS

## Development

Install dependencies.

    $ pip install -r requirements.txt

Install the app in editable mode.

    $ pip install -e .

Configure the app in `config.yml`.

Initialize the database.

    $ ./init.py

Start the app in debug mode.

    $ export FLASK_APP=workshops_api.app
    $ export FLASK_DEBUG=1
    $ flask run

## Notes

### Authentication

Some clarification on how auth works.

1. POST to /auth/login with credentials (the password) and login type (admin or user)
2. Password is checked + hash compared if admin
3. JWT token is sent as response
4. Client uses JWT token in the Authorization header to prove who he is for next requests

There are no usernames/passwords, only passwords (keys). This is for simplicity. There is no OAuth login and users change for every event, so unique keys are the most user friendly option.

These are stored in plaintext so the admin can print them, so they aren't supposed to be super secure. The admin password is hashed though.
