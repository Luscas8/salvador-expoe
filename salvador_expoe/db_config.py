import os
from pathlib import Path

# Definir BASE_DIR diretamente
BASE_DIR = Path(__file__).resolve().parent.parent

# Configurações do banco de dados
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    },
    'mysql': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'salvador_expoe',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

# Função para obter a configuração do banco de dados atual
def get_database_config():
    use_mysql = os.environ.get('USE_MYSQL', 'False').lower() == 'true'
    return DATABASES['mysql'] if use_mysql else DATABASES['default'] 