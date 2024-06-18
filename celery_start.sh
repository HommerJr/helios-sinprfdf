#!/bin/bash

# Start the Celery worker
celery -A helios.celery_app worker \
  --loglevel=info \
  --without-gossip \
  --without-mingle \
  --without-heartbeat
