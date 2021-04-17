# Use an official Python runtime based on Debian 10 "buster" as a parent image.
FROM python:3.9-slim-buster

ARG USERNAME=wagtail
ARG USER_UID=1000
ARG USER_GID=${USER_UID}

# Add user that will be used in the container.
RUN apt update --yes --quiet && apt install -y gnupg software-properties-common \
    && apt-key adv --keyserver keyserver.ubuntu.com --recv-key C99B11DEB97541F0 \
    && apt-add-repository https://cli.github.com/packages \
    && apt update --yes --quiet && apt install -y git gh \
    && groupadd --gid ${USER_GID} ${USERNAME} \
    && useradd -s /bin/bash --uid ${USER_UID} --gid ${USER_GID} -m ${USERNAME} \
    && apt install -y sudo \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME\
    && chmod 0440 /etc/sudoers.d/$USERNAME

# Port used by this container to serve HTTP.
EXPOSE 8000

# Set environment variables.
# 1. Force Python stdout and stderr streams to be unbuffered.
# 2. Set PORT variable that is used by Gunicorn. This should match "EXPOSE"
#    command.
ENV PYTHONUNBUFFERED=1 \
    PORT=8000 \
    WORKDIR=/app/

# Install system packages required by Wagtail and Django.
RUN apt update --yes --quiet && apt install --yes --quiet --no-install-recommends \
    build-essential \
    libpq-dev \
    libjpeg62-turbo-dev \
    zlib1g-dev \
    libwebp-dev \
 && rm -rf /var/lib/apt/lists/*

# Use /app folder as a directory where the source code is stored.
WORKDIR ${WORKDIR}

# Install the project requirements.
COPY Pipfile ${WORKDIR}
RUN pip install pipenv --no-cache-dir && \
    pipenv lock --clear --dev && \
    pipenv install --system --deploy --dev && \
    pip uninstall -y pipenv virtualenv-clone virtualenv

# Set this directory to be owned by the "wagtail" user. This Wagtail project
# uses SQLite, the folder needs to be owned by the user that
# will be writing to the database file.
RUN chown ${USER_GID}:${USER_UID} /app

# Copy the source code of the project into the container.
COPY --chown=${USER_GID}:${USER_UID} . .

# Use user "wagtail" to run the build commands below and the server itself.
USER ${USERNAME}

# Collect static files.
RUN python manage.py collectstatic --noinput --clear

# Runtime command that executes when "docker run" is called, it does the
# following:
#   1. Migrate the database.
#   2. Start the application server.
# WARNING:
#   Migrating database at the same time as starting the server IS NOT THE BEST
#   PRACTICE. The database should be migrated manually or using the release
#   phase facilities of your hosting platform. This is used only so the
#   Wagtail instance can be started with a simple "docker run" command.
CMD set -xe; python manage.py migrate --noinput; gunicorn huidetang.wsgi:application
