# Nome do Projeto

Uma breve descrição do que este projeto faz e quem ele é para.

## Índice

- [Sobre](#sobre)
- [Pré-requisitos](#pré-requisitos)
- [Instalação](#instalação)
- [Uso](#uso)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Documentação da API](#documentação-da-api)
- [Desenvolvimento](#desenvolvimento)
- [Produção](#produção)
- [Solução de Problemas](#solução-de-problemas)

## Sobre

Este projeto é uma aplicação web moderna que consiste em:
- Frontend em Angular
- Backend em Python (FastAPI)
- Banco de dados PostgreSQL

## Pré-requisitos

Antes de começar, você precisa ter instalado em sua máquina:
- Docker e Docker Compose
- Node.js (versão 18 ou superior) - apenas para desenvolvimento do frontend
- Python 3.8 ou superior - apenas para desenvolvimento do backend
- Git

## Instalação

1. Clone o repositório
```bash
git clone https://github.com/seu-usuario/nome-do-projeto.git
cd nome-do-projeto
```

2. Configure as variáveis de ambiente
```bash
# Copie o arquivo .env.example para .env
cp backend-python/src/.env.example backend-python/src/.env
```

3. Inicie os containers Docker
```bash
docker-compose up --build
```

## Uso

Após a instalação, você pode acessar:

- Frontend: http://localhost:4200
- Backend API: http://localhost:8000
- Documentação da API: http://localhost:8000/docs
- Banco de dados PostgreSQL:
  - Host: localhost
  - Porta: 5432
  - Usuário: postgres
  - Senha: postgres
  - Banco: app_db

## Estrutura do Projeto

```
.
├── frontend-angular/     # Frontend Angular
├── backend-python/       # Backend Python (FastAPI)
│   ├── src/
│   │   └── app/
│   │       ├── core/
│   │       │   └── config/
│   │       │       └── config.py
│   │       └── services/
│   │           └── main.py
│   ├── Dockerfile
│   └── requirements.txt
├── docker-compose.yml
└── doc/
    └── README.md
```

## Documentação da API

A documentação da API está disponível através de:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Desenvolvimento

### Frontend (Angular)

Para desenvolvimento local do frontend:

```bash
cd frontend-angular
npm install
ng serve
```

### Backend (Python/FastAPI)

Para desenvolvimento local do backend:

```bash
cd backend-python/src
pip install -r requirements.txt
uvicorn app.services.main:app --reload --host 0.0.0.0 --port 8000
```

## Produção

Para implantar em produção:

1. Configure as variáveis de ambiente de produção
2. Execute o Docker Compose em modo de produção:
```bash
docker-compose -f docker-compose.prod.yml up --build
```

## Solução de Problemas

### Docker
- Se os containers não iniciarem, verifique os logs:
  ```bash
  docker-compose logs
  ```
- Para reiniciar os containers:
  ```bash
  docker-compose down
  docker-compose up --build
  ```

### Frontend
- Se encontrar problemas de CORS, verifique se o backend está rodando
- Para limpar o cache do npm: `npm cache clean --force`
- Para reinstalar as dependências: `rm -rf node_modules && npm install`

### Backend
- Verifique se todas as dependências estão instaladas corretamente
- Para ver logs detalhados, remova a flag `--reload` do comando uvicorn

### Banco de Dados
- Para acessar o banco de dados diretamente:
  ```bash
  docker exec -it postgres_db psql -U postgres
  ```
- Para fazer backup do banco:
  ```bash
  docker exec -t postgres_db pg_dump -U postgres app_db > backup.sql
  ```

## Contribuindo

1. Faça um Fork do projeto
2. Crie sua Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a Branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## Licença

Este projeto está sob a licença [MIT](LICENSE).

## Contato

Seu Nome - [@seutwitter](https://twitter.com/seutwitter) - email@exemplo.com

Link do Projeto: [https://github.com/seu-usuario/nome-do-projeto](https://github.com/seu-usuario/nome-do-projeto) 