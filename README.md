# Salvador Expoe

Um projeto Django para avaliação e visualização de bairros de Salvador através de um mapa de calor.

## Funcionalidades

- Mapa de calor interativo dos bairros de Salvador
- Sistema de avaliação de bairros
- Painel administrativo
- Autenticação de usuários
- Visualização de avaliações recentes

## Tecnologias Utilizadas

- Python 3.10
- Django 4.2
- Folium (para mapas)
- Bootstrap 5
- SQLite (desenvolvimento e produção)
- Gunicorn (servidor WSGI)
- Nginx (servidor web)

## Instalação para Desenvolvimento

1. Clone o repositório:
```bash
git clone https://github.com/Luscas8/salvador-expoe.git
cd salvador-expoe
```

2. Crie e ative um ambiente virtual:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Execute as migrações:
```bash
python manage.py migrate
```

5. Crie um superusuário:
```bash
python manage.py createsuperuser
```

6. Inicie o servidor de desenvolvimento:
```bash
python manage.py runserver
```

## Deploy em Produção

1. Configure as variáveis de ambiente:
```bash
cp .env.example .env
# Edite o arquivo .env com suas configurações
```

2. Instale as dependências de produção:
```bash
pip install -r requirements.txt
```

3. Configure o Nginx:
```bash
# Copie o arquivo nginx.conf para /etc/nginx/sites-available/
sudo cp nginx.conf /etc/nginx/sites-available/salvador_expoe
# Crie um link simbólico
sudo ln -s /etc/nginx/sites-available/salvador_expoe /etc/nginx/sites-enabled/
# Teste a configuração
sudo nginx -t
# Reinicie o Nginx
sudo systemctl restart nginx
```

4. Configure o SSL (usando Certbot):
```bash
sudo certbot --nginx -d seu-dominio.com
```

5. Inicie a aplicação:
```bash
chmod +x start_prod.sh
./start_prod.sh
```

6. Configure o supervisor para manter a aplicação rodando:
```bash
sudo apt-get install supervisor
sudo cp salvador_expoe.conf /etc/supervisor/conf.d/
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start salvador_expoe
```

## Backup

O sistema faz backup automático do banco de dados a cada vez que é iniciado. Os backups são armazenados no diretório `backups/` e são mantidos os últimos 5 backups.

Para fazer um backup manual:
```bash
python backup_db.py
```

## Monitoramento

Os logs da aplicação são armazenados em:
- `logs/django.log` - Logs do Django
- `logs/gunicorn-access.log` - Logs de acesso do Gunicorn
- `logs/gunicorn-error.log` - Logs de erro do Gunicorn
- `logs/backup.log` - Logs de backup

## Contato

Lucas Brendo ALves Dos Santos Conceição- [@Luscas8](https://github.com/Luscas8) 
Letícia Beatriz dos Reis Gomes [@biaadeveloper](https://github.com/biaadeveloper)
