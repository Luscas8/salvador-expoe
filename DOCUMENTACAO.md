# Documentação do Projeto Salvador Expoe

## Visão Geral
O Salvador Expoe é uma plataforma web desenvolvida em Django que permite a visualização e avaliação dos bairros de Salvador através de um mapa de calor interativo. O projeto visa fornecer uma ferramenta para que os usuários possam compartilhar suas experiências e avaliações sobre diferentes bairros da cidade.

## Arquitetura do Projeto

### Tecnologias Principais
- **Backend**: Django 4.2
- **Frontend**: Bootstrap 5, HTML, CSS, JavaScript
- **Banco de Dados**: SQLite
- **Servidor Web**: Nginx
- **Servidor WSGI**: Gunicorn
- **Visualização de Mapas**: Folium
- **Autenticação**: Sistema nativo do Django
- **Formulários**: django-crispy-forms com crispy-bootstrap5

### Estrutura de Diretórios
```
salvador-expoe/
├── core/                  # Aplicação principal
├── salvador_expoe/        # Configurações do projeto
├── static/               # Arquivos estáticos
├── templates/            # Templates HTML
├── venv/                 # Ambiente virtual
└── scripts/             # Scripts utilitários
```

## Funcionalidades Principais

### 1. Sistema de Mapa de Calor
- Visualização interativa dos bairros de Salvador
- Cores dinâmicas baseadas nas avaliações
- Zoom e navegação intuitiva
- Informações detalhadas ao clicar nos bairros

### 2. Sistema de Avaliações
- Interface para adicionar avaliações
- Sistema de pontuação
- Comentários e feedback
- Histórico de avaliações

### 3. Autenticação e Usuários
- Registro de usuários
- Login/Logout
- Perfis de usuário
- Níveis de acesso (admin/usuário comum)

### 4. Painel Administrativo
- Gerenciamento de usuários
- Moderação de avaliações
- Estatísticas e relatórios
- Configurações do sistema

## APIs e Endpoints

### Endpoints Principais
- `/api/bairros/` - Lista e detalhes dos bairros
- `/api/avaliacoes/` - Gerenciamento de avaliações
- `/api/usuarios/` - Operações relacionadas a usuários
- `/api/estatisticas/` - Dados estatísticos do sistema

## Scripts Utilitários

### Scripts de Manutenção
- `backup_db.py` - Backup do banco de dados
- `gerar_mapa_calor.py` - Geração do mapa de calor
- `verificar_dados.py` - Verificação de integridade dos dados
- `adicionar_coordenadas.py` - Adição de coordenadas aos bairros

### Scripts de Desenvolvimento
- `popular_dados_teste.py` - População do banco com dados de teste
- `reset_db.py` - Reset do banco de dados
- `create_superuser.py` - Criação de superusuário

## Configuração e Deploy

### Requisitos do Sistema
- Python 3.10+
- Nginx
- Gunicorn
- SQLite

### Variáveis de Ambiente
- `DEBUG` - Modo de debug
- `SECRET_KEY` - Chave secreta do Django
- `ALLOWED_HOSTS` - Hosts permitidos
- `DATABASE_URL` - URL do banco de dados

### Processo de Deploy
1. Configuração do ambiente
2. Instalação de dependências
3. Configuração do Nginx
4. Configuração do SSL
5. Inicialização do Gunicorn
6. Configuração do Supervisor

## Segurança

### Medidas Implementadas
- Rate limiting para APIs
- Proteção contra CSRF
- Validação de dados
- Sanitização de inputs
- Autenticação segura
- Headers de segurança

## Monitoramento e Manutenção

### Logs
- Logs do Django
- Logs do Gunicorn
- Logs de backup
- Logs de erro

### Backup
- Backup automático diário
- Retenção dos últimos 5 backups
- Script de backup manual disponível

## Contribuição
Para contribuir com o projeto:
1. Fork o repositório
2. Crie uma branch para sua feature
3. Faça commit das mudanças
4. Push para a branch
5. Crie um Pull Request

## Contato
- Lucas Brendo Alves Dos Santos Conceição - [@Luscas8](https://github.com/Luscas8)
- Letícia Beatriz dos Reis Gomes - [@biaadeveloper](https://github.com/biaadeveloper) 