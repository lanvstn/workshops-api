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

## Installing in production

There are many ways to deploy this application. This is an example.

Prerequisites:

* Preferably a Linux based server, I haven't tested this on Windows.
* Python 3 with an up to date pip.
* SQLite, Postgresql, MySQL or Oracle.

I recommend installing the front end first, so you already have an nginx running. You could use the same nginx as you are using for the front end.

Create a user for workshops-api.

Clone this project to `/home/workshops-api/workshops-api` and cd into it.

Install dependencies.

    # pip install -r requirements.txt

Install this module. *(note: this project is not in the pip repositories)*

    # pip install .

Configure the app in `config.yml`.

Initialize the database.

    $ ./init.py

**Nginx**

Create a new file in `/etc/nginx/sites-available/workshops-api`


```
upstream app_server {
    server unix:/run/gunicorn/socket;
}


server {
    # CHANGE THIS
    server_name api.workshops.example.com;

    root /var/www/workshops-api; # empty directory

    location / {
        try_files $uri @app;
    }

    location @app {
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header Host $http_host;
        proxy_redirect off;
        proxy_pass http://app_server;
    }
}
```

Link it to sites-enabled:

    # ln -s /etc/nginx/sites-available/workshops-api /etc/nginx/sites-enabled/workshops-api

[Information about nginx and systemd in the gunicorn docs.](http://docs.gunicorn.org/en/stable/deploy.html#nginx-configuration)

**Systemd**

Create a socket `/etc/systemd/system/gunicorn.socket`

```
[Unit]
Description=gunicorn socket

[Socket]
ListenStream=/run/gunicorn/socket

[Install]
WantedBy=sockets.target
```

And a service `/etc/systemd/system/gunicorn.service`

```
[Unit]
Description=gunicorn daemon
Requires=gunicorn.socket
After=network.target

[Service]
PIDFile=/run/gunicorn/pid
User=workshops-api
Group=workshops-api
RuntimeDirectory=gunicorn
WorkingDirectory=/home/workshops-api/workshops-api
ExecStart=/usr/local/bin/gunicorn --pid /run/gunicorn/pid   \
          --bind unix:/run/gunicorn/socket workshops_api.app:app
ExecReload=/bin/kill -s HUP $MAINPID
ExecStop=/bin/kill -s TERM $MAINPID
PrivateTmp=true

[Install]
WantedBy=multi-user.target
```

Refresh systemd config, enable your new service at boot and start the app.

    # systemctl daemon-reload
    # systemctl enable gunicorn.socket gunicorn.service 
    # systemctl start gunicorn.socket gunicorn.service
    # systemctl restart nginx.service

Make sure everything is running.

    # systemctl status gunicorn.socket gunicorn.service nginx.service

Try to access the site. If it doesn't work, read the logs.

**Set up HTTPS**

You have no excuse not to use HTTPS. It's free and easy to set up. 

Read the instructions: [Let's encrypt](https://certbot.eff.org/lets-encrypt/ubuntubionic-nginx)


## Running for development and testing

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
