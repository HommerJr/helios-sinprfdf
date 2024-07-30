#!/bin/bash

# Função para aguardar o banco de dados estar pronto
wait_for_db() {
    echo "Aguardando o banco de dados Postgres..."
    while ! nc -z db 5432; do
        sleep 1
    done
}

# Compile messages for internationalization
compile_messages() {
    echo "Compilando mensagens para internacionalização..."
    python manage.py compilemessages
}

# Apply database migrations
apply_migrations() {
    echo "Aplicando migrações do banco de dados..."
    python manage.py migrate
}

# Create a superuser if needed
create_superuser() {
    if [ "$DJANGO_CREATE_SUPERUSER" = "true" ]; then
        echo "Criando superusuário..."
        python manage.py shell <<EOF
from django.contrib.auth.models import User;
from django.contrib.auth.hashers import make_password;
if not User.objects.filter(username='$DJANGO_SUPERUSER_USERNAME').exists():
    User.objects.create_superuser(username='$DJANGO_SUPERUSER_USERNAME', email='$DJANGO_SUPERUSER_EMAIL', password='$DJANGO_SUPERUSER_PASSWORD')
EOF
    fi
}

# Main execution
main() {
    wait_for_db
    compile_messages
    apply_migrations
    create_superuser
    echo "Iniciando o servidor Django..."
    exec "$@"
}

main