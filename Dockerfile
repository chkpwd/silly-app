FROM python:3.13-slim-bookworm AS base

ENV PYTHONUNBUFFERED=1 \
    PYTHONFAULTHANDLER=1

WORKDIR /app

FROM base AS builder

ENV PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VERSION=1.8

RUN pip install "poetry==$POETRY_VERSION"

COPY poetry.lock pyproject.toml ./

RUN poetry config virtualenvs.in-project true && \
    poetry lock --no-update && \
    poetry install --only=main

FROM base AS final

RUN adduser -u 1000 python

RUN chown -R python:python /app/images

USER python

ENV DEBUG=false \
    UVICORN_HOST="0.0.0.0" \
    UVICORN_PORT="8000"

COPY --from=builder /app/.venv ./.venv
COPY main.py .

ENTRYPOINT ["/app/.venv/bin/uvicorn", "main:app", "--reload"]
