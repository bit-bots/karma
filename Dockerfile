FROM debian:buster

RUN apt update
RUN apt -y --no-install-recommends install g++ uwsgi uwsgi-plugin-python3 python3 python3-pip virtualenv make python3-psycopg2 python3-ldap3 gettext gcc python3-dev libldap2-dev libsasl2-dev

RUN usermod -u 2012 -g 33 -d /opt/karma www-data

WORKDIR /opt/karma
ADD . /opt/karma

RUN pip3 install pipenv
ENV PIPENV_VENV_IN_PROJECT=1
RUN pipenv sync
RUN pipenv install psycopg2-binary django-ldapdb django-auth-ldap uwsgi requests sentry-sdk coreapi

RUN ln -sf /opt/config/settings.py /opt/karma/karma/settings.py
RUN ln -sf /opt/static/ /opt/karma/_static

COPY docker/uwsgi-karma.ini /etc/uwsgi/karma.ini
COPY docker/run /usr/local/bin/run

VOLUME /opt/static
VOLUME /opt/config
VOLUME /opt/storage

USER www-data:www-data

ENTRYPOINT /usr/local/bin/run
