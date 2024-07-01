# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    libsasl2-dev \
    libldap2-dev \
    libssl-dev \
    openssl \
    gettext \
    libffi-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install pip dependencies
COPY ../requirements.txt /app/
RUN pip install --upgrade pip \
    && pip install -r requirements.txt gunicorn

# Copy the application code
COPY . /app/

# Change the ownership of the application files
RUN chown -R helios:helios /app \
    && chmod +x /app/celery_start.sh

# Switch to 'helios' user
USER helios

# Run the entrypoint script
RUN chmod +x /app/entrypoint.sh
ENTRYPOINT ["/app/entrypoint.sh"]
