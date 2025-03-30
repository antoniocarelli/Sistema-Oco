# Sistema oco
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]

<!-- LOGO DO PROJETO -->
<br />
<div align="center">
  <a href="https://github.com/antoniocarelli/Sistema-Oco">
    <img src="images/logo.png" alt="Logo" width="100%" height="100%">
  </a>

  <h3 align="center">Sistema oco</h3>

  <p align="center">
    Uma arquitetura completa e integrada com as três camadas essenciais (frontend, backend e banco de dados) funcionando em perfeita harmonia.
    <br />
    Implementa um sistema robusto de autenticação que inclui cadastro de usuários, login seguro e mecanismo de recuperação de senha.
    <br />
    <a href="https://github.com/antoniocarelli/Sistema-Oco"><strong>Explore a documentação</strong></a>
    <br />
    <a href="https://github.com/antoniocarelli/Sistema-Oco/issues">Reportar Bug</a>
    ·
    <a href="https://github.com/antoniocarelli/Sistema-Oco/issues">Solicitar Funcionalidade</a>
  </p>
</div>

<!-- ÍNDICE -->
<details>
  <summary>Índice</summary>
  <ol>
    <li>
      <a href="#sobre-o-projeto">Sobre o Projeto</a>
      <ul>
        <li><a href="#construído-com">Construído Com</a></li>
      </ul>
    </li>
    <li>
      <a href="#começando">Começando</a>
      <ul>
        <li><a href="#pré-requisitos">Pré-requisitos</a></li>
        <li><a href="#instalação">Instalação</a></li>
      </ul>
    </li>
    <li><a href="#uso">Uso</a></li>
    <li><a href="#estrutura-do-projeto">Estrutura do Projeto</a></li>
    <li><a href="#documentação-da-api">Documentação da API</a></li>
    <li><a href="#desenvolvimento">Desenvolvimento</a></li>
    <li><a href="#produção">Produção</a></li>
    <li><a href="#solução-de-problemas">Solução de Problemas</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contribuindo">Contribuindo</a></li>
    <li><a href="#licença">Licença</a></li>
    <li><a href="#contato">Contato</a></li>
    <li><a href="#agradecimentos">Agradecimentos</a></li>
  </ol>
</details>

<!-- SOBRE O PROJETO -->
## Sobre o Projeto

![Captura de Tela do Produto][product-screenshot]

Este projeto é uma aplicação web moderna que consiste em:
* Frontend em Angular
* Backend em Python (FastAPI)
* Banco de dados PostgreSQL

O diferencial deste projeto é que foi desenvolvido integralmente utilizando Inteligência Artificial, sem nenhuma intervenção manual no código. Todo o desenvolvimento foi realizado com o auxílio do Cursor IDE, configurado com o modelo Claude 3.7 Sonnet como IA principal.


<p align="right">(<a href="#sistema-oco">voltar ao topo</a>)</p>

### Construído Com

* [![Angular][Angular.io]][Angular-url]
* [![FastAPI][FastAPI]][FastAPI-url]
* [![PostgreSQL][PostgreSQL]][PostgreSQL-url]
* [![Docker][Docker]][Docker-url]

<p align="right">(<a href="#sistema-oco">voltar ao topo</a>)</p>

<!-- COMEÇANDO -->
## Começando

Para obter uma cópia local em funcionamento, siga estas etapas simples.

### Pré-requisitos

Antes de começar, você precisa ter instalado em sua máquina:
* Docker e Docker Compose
* Node.js (versão 18 ou superior) - apenas para desenvolvimento do frontend
* Python 3.8 ou superior - apenas para desenvolvimento do backend
* Git

### Instalação

1. Clone o repositório
   ```sh
   git clone https://github.com/antoniocarelli/Sistema-Oco.git
   cd nome-do-projeto
   ```
2. Configure as variáveis de ambiente
   ```sh
   # Copie o arquivo .env.example para .env
   cp backend-python/src/.env.example backend-python/src/.env
   ```
3. Inicie os containers Docker
   ```sh
   docker-compose up --build
   ```

<p align="right">(<a href="#sistema-oco">voltar ao topo</a>)</p>

<!-- USO -->
## Uso

Após a instalação, você pode acessar:

* Frontend: http://localhost:4200
* Backend API: http://localhost:8000
* Documentação da API: http://localhost:8000/docs
* Banco de dados PostgreSQL:
  * Host: localhost
  * Porta: 5432
  * Usuário: postgres
  * Senha: postgres
  * Banco: app_db

<p align="right">(<a href="#sistema-oco">voltar ao topo</a>)</p>

<!-- ESTRUTURA DO PROJETO -->
## Estrutura do Projeto

```
.
├── frontend-angular/           # Frontend Angular
│   ├── src/
│   │   ├── app/                # Código da aplicação Angular
│   │   │   ├── components/     # Componentes reutilizáveis
│   │   │   ├── pages/          # Componentes de página
│   │   │   ├── services/       # Serviços para comunicação com a API
│   │   │   ├── app.routes.ts   # Configuração de rotas
│   │   │   └── app.config.ts   # Configurações da aplicação
│   │   ├── environments/       # Configurações de ambiente (dev/prod)
│   │   └── assets/             # Imagens e outros recursos estáticos
│   ├── Dockerfile              # Configuração para build do frontend
│   ├── nginx.conf              # Configuração do servidor web Nginx
│   ├── package.json            # Dependências do projeto
│   └── angular.json            # Configuração do Angular CLI
│
├── backend-python/             # Backend Python (FastAPI)
│   ├── src/
│   │   ├── app/
│   │   │   ├── core/           # Componentes principais da aplicação
│   │   │   │   └── config/     # Configurações do aplicativo
│   │   │   ├── models/         # Modelos de dados e ORM
│   │   │   ├── routes/         # Definições de endpoints da API
│   │   │   ├── schemas/        # Esquemas Pydantic para validação
│   │   │   ├── services/       # Lógica de negócios
│   │   │   │   └── main.py     # Ponto de entrada da aplicação
│   │   │   └── utils/          # Funções utilitárias
│   │   ├── config/             # Configurações de ambiente
│   │   ├── tests/              # Testes unitários e de integração
│   │   └── .env.example        # Exemplo de variáveis de ambiente
│   ├── alembic/                # Migrações de banco de dados
│   ├── Dockerfile              # Configuração para build do backend
│   └── requirements.txt        # Dependências Python
│
├── docker-compose.yml          # Configuração do Docker Compose para desenvolvimento
├── doc/                        # Documentação adicional do projeto
├── images/                     # Imagens usadas no README
└── LICENSE                     # Licença do projeto
```

<p align="right">(<a href="#sistema-oco">voltar ao topo</a>)</p>

<!-- DOCUMENTAÇÃO DA API -->
## Documentação da API

A documentação da API está disponível através de:
* Swagger UI: http://localhost:8000/docs
* ReDoc: http://localhost:8000/redoc

<p align="right">(<a href="#sistema-oco">voltar ao topo</a>)</p>

<!-- DESENVOLVIMENTO -->
## Desenvolvimento

### Frontend (Angular)

Para desenvolvimento local do frontend:

```sh
cd frontend-angular
npm install
ng serve
```

### Backend (Python/FastAPI)

Para desenvolvimento local do backend:

```sh
cd backend-python/src
pip install -r requirements.txt
uvicorn app.services.main:app --reload --host 0.0.0.0 --port 8000
```

<p align="right">(<a href="#sistema-oco">voltar ao topo</a>)</p>

<!-- PRODUÇÃO -->
## Produção

Para implantar em produção:

1. Configure as variáveis de ambiente de produção
2. Execute o Docker Compose em modo de produção:
   ```sh
   docker-compose -f docker-compose.prod.yml up --build
   ```

<p align="right">(<a href="#sistema-oco">voltar ao topo</a>)</p>

<!-- SOLUÇÃO DE PROBLEMAS -->
## Solução de Problemas

### Docker
* Se os containers não iniciarem, verifique os logs:
  ```sh
  docker-compose logs
  ```
* Para reiniciar os containers:
  ```sh
  docker-compose down
  docker-compose up --build
  ```

### Frontend
* Se encontrar problemas de CORS, verifique se o backend está rodando
* Para limpar o cache do npm: `npm cache clean --force`
* Para reinstalar as dependências: `rm -rf node_modules && npm install`

### Backend
* Verifique se todas as dependências estão instaladas corretamente
* Para ver logs detalhados, remova a flag `--reload` do comando uvicorn

### Banco de Dados
* Para acessar o banco de dados diretamente:
  ```sh
  docker exec -it postgres_db psql -U postgres
  ```
* Para fazer backup do banco:
  ```sh
  docker exec -t postgres_db pg_dump -U postgres app_db > backup.sql
  ```

<p align="right">(<a href="#sistema-oco">voltar ao topo</a>)</p>

<!-- ROADMAP -->
## Roadmap

* [ ] Login com Google
* [ ] Login com Facebook


Veja os [issues abertos](https://github.com/antoniocarelli/Sistema-Oco/issues) para uma lista completa de funcionalidades propostas (e problemas conhecidos).

<p align="right">(<a href="#sistema-oco">voltar ao topo</a>)</p>

<!-- CONTRIBUINDO -->
## Contribuindo

Contribuições são o que tornam a comunidade open source um lugar incrível para aprender, inspirar e criar. Quaisquer contribuições que você fizer são **muito apreciadas**.

Se você tem uma sugestão para melhorar isso, faça um fork do repositório e crie um pull request. Você também pode simplesmente abrir um issue com a tag "melhoria".
Não se esqueça de dar uma estrela ao projeto! Obrigado novamente!

1. Faça um Fork do projeto
2. Crie sua Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a Branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

<p align="right">(<a href="#sistema-oco">voltar ao topo</a>)</p>

<!-- LICENÇA -->
## Licença

Distribuído sob a licença MIT. Veja `LICENSE` para mais informações.

<p align="right">(<a href="#sistema-oco">voltar ao topo</a>)</p>

<!-- CONTATO -->
## Contato

Antonio Carelli: [LinkedIn][linkedin-url]

Link do Projeto: [GitHub](https://github.com/antoniocarelli/Sistema-Oco)

<p align="right">(<a href="#sistema-oco">voltar ao topo</a>)</p>


<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[license-shield]: https://img.shields.io/github/license/antoniocarelli/Sistema-Oco.svg?style=for-the-badge
[license-url]: https://github.com/antoniocarelli/Sistema-Oco/blob/main/LICENSE
[linkedin-shield]: https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white
[linkedin-url]: https://www.linkedin.com/in/antonio-carelli/
[product-screenshot]: images/screenshot.jpeg
[Angular.io]: https://img.shields.io/badge/Angular-DD0031?style=for-the-badge&logo=angular&logoColor=white
[Angular-url]: https://angular.io/
[FastAPI]: https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white
[FastAPI-url]: https://fastapi.tiangolo.com/
[PostgreSQL]: https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white
[PostgreSQL-url]: https://www.postgresql.org/
[Docker]: https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white
[Docker-url]: https://www.docker.com/ 