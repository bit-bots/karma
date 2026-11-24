FROM ghcr.io/astral-sh/uv:python3.12-trixie-slim AS base

ENV UV_PYTHON_DOWNLOADS=never \
    UV_LINK_MODE=copy \
    PATH="/opt/karma/.venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /opt/karma

FROM base AS builder

RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential libpcre2-dev \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml uv.lock .python-version ./
# The application runs from /opt/karma; only its dependencies are installed here.
RUN uv sync --locked --group docker --no-install-project --compile-bytecode

FROM base AS runtime

RUN apt-get update \
    && apt-get install -y --no-install-recommends gettext libpcre2-8-0 \
    && rm -rf /var/lib/apt/lists/* \
    && usermod -u 33 -g 33 -d /opt/karma www-data \
    && mkdir -p /opt/config /opt/static /opt/storage \
    && chown www-data:www-data /opt/static /opt/storage

COPY --from=builder /opt/karma/.venv /opt/karma/.venv
COPY karma ./karma
COPY manage.py ./manage.py

RUN python -m compileall -q /opt/karma/karma /opt/karma/manage.py \
    && ln -sf /opt/config/settings.py /opt/karma/karma/settings.py \
    && ln -sf /opt/static /opt/karma/_static

COPY docker/uwsgi-karma.ini /etc/uwsgi/karma.ini
COPY --chmod=755 docker/run /usr/local/bin/run

VOLUME ["/opt/static", "/opt/config", "/opt/storage"]

USER www-data:www-data

ENTRYPOINT ["/usr/local/bin/run"]
