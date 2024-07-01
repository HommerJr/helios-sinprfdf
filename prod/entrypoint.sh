#!/bin/bash

# Compile messages for internationalization
python manage.py compilemessages

# Apply database migrations
python manage.py migrate

# Check if a superuser needs to be created (preferably use environment variables for production deployment)
if [ "$DJANGO_CREATE_SUPERUSER" = "true" ]; then
    echo "Creating superuser..."
    echo "from django.contrib.auth.models import User;
    from django.contrib.auth.hashers import make_password;
    if not User.objects.filter(username='$DJANGO_SUPERUSER_USERNAME').exists():
        User.objects.create_superuser(username='$DJANGO_SUPERUSER_USERNAME', email='$DJANGO_SUPERUSER_EMAIL', password='$DJANGO_SUPERUSER_PASSWORD')" | python manage.py shell
fi

# Start the Django server
exec "$@"
