# syntax=docker/dockerfile:1

# Comments are provided throughout this file to help you get started.
# If you need more help, visit the Dockerfile reference guide at
# https://docs.docker.com/engine/reference/builder/

ARG PYTHON_VERSION=3.11.4
FROM python:${PYTHON_VERSION}-slim as base

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1

# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1

WORKDIR .

# Create a non-privileged user that the app will run under.
# See https://docs.docker.com/go/dockerfile-user-best-practices/
ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser

# Install curl and Poetry
RUN apt-get update && apt-get install -y curl libffi-dev libpq-dev build-essential&& \
    curl -sSL https://install.python-poetry.org | python3 -

# Add Poetry to the PATH
ENV PATH="/root/.local/bin:${PATH}"

# Configure Poetry
RUN poetry config virtualenvs.create false && \
    which poetry

# Copy pyproject.toml and poetry.lock separately to leverage Docker caching
COPY pyproject.toml poetry.lock ./

# Download dependencies as a separate step to take advantage of Docker's caching.
# Leverage a cache mount to /root/.cache/pip to speed up subsequent builds.
RUN --mount=type=cache,target=/root/.cache/pip \
    poetry install --no-interaction --no-ansi

# Switch to the non-privileged user to run the application.
USER root
# changue to appuser in production

# Copy the source code into the container.
COPY . .

# Expose the port that the application listens on.
EXPOSE 8000