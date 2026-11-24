# Karma

Karma is a simple time tracking system.

## Features

* projects
* categories
* project highscores
* command line interface

## Installation

Install [uv](https://docs.astral.sh/uv/getting-started/installation/) to manage Python
and the project virtual environment. The checked-in `.python-version` selects Python 3.11.
Install the locked dependencies with

```
uv sync --locked
```

The application dependencies are declared in `pyproject.toml` and locked in `uv.lock`.
Commit both files when changing dependencies.

`uv sync` installs the application as an editable package. Run `uv build` to build
a source distribution and wheel.

Copy settings.py.example to settings.py in the karma folder:

```
cp karma/settings.py.example karma/settings.py
```

and customize the settings.py.

The following settings should probably be changed:

+ The secret key
+ The DEBUG setting
+ The ALLOWED\_HOSTS
+ The database settings

For instructions on how to use other databases than sqlite, have a look at the [Django
Documentation](https://docs.djangoproject.com/en/3.0/ref/settings/#std:setting-DATABASES).

To initialize the database, run `uv run --locked ./manage.py migrate`

To create an administrator user, run `uv run --locked ./manage.py createsuperuser`.

`uv run --locked ./manage.py runserver` starts the server with the configuration given in the settings.py file.

On the website, you can use the *Add Project* or *Add Category* buttons to add projects and
categories.

Since we use the karma system with LDAP, there is currently no registration interface. You can
instead create users using `uv run --locked ./manage.py createsuperuser` or in the django admin
interface which is located at `/admin`. Navigate to Users -> Add user and insert the user data.
If you also want to use LDAP for authentication, use `django-auth-ldap`. For configuration, have a
look at [their GitHub page](https://github.com/django-auth-ldap/django-auth-ldap) or
[their documentation](https://django-auth-ldap.readthedocs.io/).

For **production** systems it is necessary to additionally run the command `uv run --locked ./manage.py
collectstatic`. For production, we recommend to use uwsgi.

## Docker

Build the image with:

```sh
docker build -t karma .
```

Create a configuration directory containing your customized `settings.py`. For
container deployments, set `STATIC_ROOT = '/opt/static'` and use `/opt/storage`
for persistent database files (for example, `/opt/storage/db.sqlite3` for SQLite).
Configure `ALLOWED_HOSTS`, the secret key, and OpenID settings for your deployment.

```sh
docker run --rm --name karma \
  --mount type=bind,src=/absolute/path/to/config,dst=/opt/config,readonly \
  --mount type=volume,src=karma-static,dst=/opt/static \
  --mount type=volume,src=karma-storage,dst=/opt/storage \
  -p 3005:3005 karma
```

The container runs as UID 33 and GID 33. Mounted configuration must be readable
by this user; storage and static directories must be writable. Startup applies
migrations and collects static files before starting uWSGI on port 3005, using
the uWSGI protocol. Configure a reverse proxy with uWSGI support in front of it.

The `docker` dependency group contains uWSGI and is installed during the image
build. Add any drivers or integrations required by your deployment settings to
the project dependencies and update `uv.lock` before building the image.
