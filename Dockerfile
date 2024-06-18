# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/

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
    && rm -rf /var/lib/apt/lists/*
# Create celeryuser
RUN useradd -ms /bin/bash celeryuser

# Install pip dependencies
RUN pip install --upgrade pip
COPY requirements.txt /app/
RUN pip install -r requirements.txt gunicorn

# Create SSL certificate
RUN openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /etc/ssl/private/selfsigned.key -out /etc/ssl/certs/selfsigned.crt -subj "/C=US/ST=Denial/L=Springfield/O=Dis/CN=localhost"

# Copy the application code
COPY . /app/

# Ensure reset.sh is executable
RUN chmod +x /app/entrypoint.sh

# Change ownership of the app directory to celeryuser
RUN chown -R celeryuser:celeryuser /app

# Run the entrypoint script
ENTRYPOINT ["/app/entrypoint.sh"]
