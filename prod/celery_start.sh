#!/bin/bash

# Start the Celery worker
# Adapte este valor conforme necessário
# Adicione limites de tempo para tarefas, se necessário
# Limites suaves podem ser ajustados conforme necessário
celery -A helios.celery_app worker \
  --loglevel=info \
  --concurrency=4 \
  --without-gossip \
  --without-mingle \
  --without-heartbeat \
  --time-limit=300 \
  --soft-time-limit=250
