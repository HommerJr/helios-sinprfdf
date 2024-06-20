#!/bin/bash

# Run migrations and create superuser
python manage.py compilemessages
python manage.py makemigrations
python manage.py migrate
echo "from django.contrib.auth.models import User;
from django.contrib.auth.hashers import make_password;
if not User.objects.filter(username='$DJANGO_SUPERUSER_USERNAME').exists():
    User.objects.create(is_staff=True, is_superuser=True, username='$DJANGO_SUPERUSER_USERNAME', email='$DJANGO_SUPERUSER_EMAIL', password=make_password('$DJANGO_SUPERUSER_PASSWORD'))" | python manage.py shell

# Start the Django server
exec "$@"
