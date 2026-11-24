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

Our uwsgi configuration and a **Dockerfile** can be found at
https://github.com/fsinfuhh/dockerfiles/tree/master/karma.
