#!/bin/bash

# Criar diretórios necessários
mkdir -p logs
mkdir -p backups
mkdir -p staticfiles

# Coletar arquivos estáticos
python manage.py collectstatic --noinput

# Fazer backup do banco de dados
python backup_db.py

# Iniciar o Gunicorn
gunicorn -c gunicorn_config.py salvador_expoe.wsgi:application 