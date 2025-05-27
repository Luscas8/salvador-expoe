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
- SQLite (desenvolvimento) / MySQL (produção)

## Instalação

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

6. Inicie o servidor:
```bash
python manage.py runserver
```

## Uso

- Acesse http://localhost:8000 para ver o site
- Acesse http://localhost:8000/admin para o painel administrativo

## Contribuição

1. Faça um Fork do projeto
2. Crie uma Branch para sua Feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a Branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## Contato

Lucas Breno - [@Luscas8](https://github.com/Luscas8) 