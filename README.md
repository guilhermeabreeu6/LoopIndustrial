# TechBridge / LoopIndustrial

## Visão Geral do Projeto

O **TechBridge / LoopIndustrial** é uma plataforma digital B2B voltada para indústria inteligente, economia circular e reaproveitamento de resíduos industriais.

O objetivo principal da plataforma é conectar empresas que geram resíduos industriais com empresas que podem reutilizar esses materiais como matéria-prima, transformando descarte em oportunidade de negócio.

A proposta do projeto é unir sustentabilidade, tecnologia e vantagem competitiva por meio de um marketplace industrial funcional.

---

## Problema

Muitas empresas industriais descartam materiais com potencial de reaproveitamento porque não possuem uma forma eficiente de se conectar com outras empresas que poderiam utilizar esses resíduos como insumos produtivos.

Esse cenário gera:

- Custos de descarte;
- Perda de materiais reutilizáveis;
- Maior impacto ambiental;
- Falta de rastreabilidade;
- Desconexão entre empresas da cadeia produtiva.

---

## Solução

O **LoopIndustrial** funciona como um marketplace inteligente da economia circular.

A plataforma permite que empresas:

- Cadastrem resíduos industriais;
- Encontrem materiais disponíveis no marketplace;
- Demonstrem interesse em resíduos de outras empresas;
- Aceitem ou rejeitem negociações;
- Finalizem transações;
- Acompanhem indicadores no dashboard;
- Visualizem estimativas de impacto ambiental.

---

## Funcionalidades Implementadas

### Empresas

- Cadastro de empresas;
- Login de empresas;
- Autenticação com JWT;
- Proteção de rotas privadas;
- Consulta dos dados da empresa logada.

Rotas principais:

```http
POST /companies/register
POST /companies/login
GET /companies/me
```

---

### Resíduos

- Cadastro de resíduos industriais;
- Listagem pública de resíduos disponíveis;
- Busca textual;
- Filtros por material, cidade, estado, quantidade mínima e status;
- Listagem dos resíduos da empresa logada;
- Edição de resíduos;
- Alteração de status;
- Exclusão de resíduos;
- Exibição dos dados da empresa dona do resíduo.

Rotas principais:

```http
POST /residues
GET /residues
GET /residues/my-residues
GET /residues/{residue_id}
PUT /residues/{residue_id}
PATCH /residues/{residue_id}/status
DELETE /residues/{residue_id}
```

---

### Interesses entre Empresas

- Criação de interesse em um resíduo;
- Impedimento de interesse no próprio resíduo;
- Impedimento de interesse duplicado;
- Listagem de interesses enviados;
- Listagem de interesses recebidos;
- Aceite de interesse;
- Rejeição de interesse;
- Cancelamento de interesse;
- Reserva automática do resíduo quando o interesse é aceito;
- Finalização de negociação.

Rotas principais:

```http
POST /interests/residues/{residue_id}
GET /interests/sent
GET /interests/received
PATCH /interests/{interest_id}/status
PATCH /interests/{interest_id}/complete
```

---

### Transações

Quando uma negociação é finalizada, o sistema cria automaticamente uma transação.

A transação registra:

- Resíduo negociado;
- Empresa vendedora;
- Empresa compradora;
- Interesse que originou a negociação;
- Tipo de material;
- Quantidade;
- Unidade;
- Status;
- Observações finais;
- Data de conclusão.

Rotas principais:

```http
GET /transactions
GET /transactions/sales
GET /transactions/purchases
```

---

### Dashboard

O dashboard resume os principais dados da empresa logada.

Indicadores disponíveis:

- Total de resíduos cadastrados;
- Resíduos disponíveis;
- Resíduos reservados;
- Resíduos vendidos;
- Resíduos inativos;
- Interesses enviados;
- Interesses recebidos;
- Interesses pendentes recebidos;
- Interesses aceitos recebidos;
- Vendas concluídas;
- Compras concluídas.

Rota principal:

```http
GET /dashboard/summary
```

---

### Impacto Ambiental

O sistema possui uma estimativa inicial de CO₂ evitado com base nas transações concluídas.

A lógica considera:

- Quantidade negociada;
- Tipo de material;
- Fator estimado de impacto por material.

Rota principal:

```http
GET /impact/summary
```

Observação: os fatores de CO₂ usados atualmente são estimativas para fins de MVP e demonstração. Em uma versão futura, esses fatores devem ser substituídos por uma base técnica validada.

---

## Frontend Implementado

O frontend foi desenvolvido com **HTML, CSS e JavaScript puro**, consumindo a API FastAPI por meio de `fetch`.

Telas implementadas:

- Landing page;
- Cadastro de empresa;
- Login;
- Dashboard;
- Marketplace;
- Meus resíduos;
- Interesses;
- Transações.

### Páginas

```text
frontend/
│
├── index.html
│
├── css/
│   └── style.css
│
├── js/
│   ├── api.js
│   ├── auth.js
│   ├── dashboard.js
│   ├── marketplace.js
│   ├── residues.js
│   ├── interests.js
│   └── transactions.js
│
└── pages/
    ├── login.html
    ├── register.html
    ├── dashboard.html
    ├── marketplace.html
    ├── my-residues.html
    ├── interests.html
    └── transactions.html
```

---

## Tecnologias Utilizadas

### Backend

- Python;
- FastAPI;
- SQLAlchemy;
- PostgreSQL;
- Pydantic;
- JWT Authentication;
- Python Jose;
- Passlib com bcrypt;
- Python Dotenv;
- Uvicorn.

### Frontend

- HTML;
- CSS;
- JavaScript;
- Fetch API;
- LocalStorage;
- Live Server.

### Banco de Dados

- PostgreSQL.

---

## Estrutura Atual do Projeto

```text
TechBridge/
│
├── backend/
│   ├── venv/
│   │
│   ├── app/
│   │   ├── auth/
│   │   │   ├── dependencies.py
│   │   │   ├── hashing.py
│   │   │   └── jwt_handler.py
│   │   │
│   │   ├── database/
│   │   │   ├── base.py
│   │   │   └── db.py
│   │   │
│   │   ├── models/
│   │   │   ├── company.py
│   │   │   ├── residue.py
│   │   │   ├── interest.py
│   │   │   └── transaction.py
│   │   │
│   │   ├── routes/
│   │   │   ├── company_routes.py
│   │   │   ├── residue_routes.py
│   │   │   ├── interest_routes.py
│   │   │   ├── transaction_routes.py
│   │   │   ├── dashboard_routes.py
│   │   │   └── impact_routes.py
│   │   │
│   │   ├── schemas/
│   │   │   ├── company_schema.py
│   │   │   ├── residue_schema.py
│   │   │   ├── interest_schema.py
│   │   │   ├── transaction_schema.py
│   │   │   ├── dashboard_schema.py
│   │   │   └── impact_schema.py
│   │   │
│   │   ├── services/
│   │   │   └── impact_service.py
│   │   │
│   │   └── main.py
│   │
│   ├── .env
│   ├── .env.example
│   └── requirements.txt
│
├── frontend/
│   ├── assets/
│   ├── css/
│   │   └── style.css
│   │
│   ├── js/
│   │   ├── api.js
│   │   ├── auth.js
│   │   ├── dashboard.js
│   │   ├── marketplace.js
│   │   ├── residues.js
│   │   ├── interests.js
│   │   └── transactions.js
│   │
│   ├── pages/
│   │   ├── login.html
│   │   ├── register.html
│   │   ├── dashboard.html
│   │   ├── marketplace.html
│   │   ├── my-residues.html
│   │   ├── interests.html
│   │   └── transactions.html
│   │
│   └── index.html
│
├── .gitignore
└── README.md
```

---

## Banco de Dados

Banco utilizado:

```text
PostgreSQL
```

Nome usado no ambiente local:

```text
techbridge_db
```

Tabelas principais:

```text
companies
residues
interests
transactions
```

---

## Configuração do Ambiente

### 1. Clonar o repositório

```bash
git clone URL_DO_REPOSITORIO
cd TechBridge
```

### 2. Criar ambiente virtual

Dentro da pasta `backend`:

```bash
python -m venv venv
```

### 3. Ativar ambiente virtual no Windows

```bash
.\venv\Scripts\Activate
```

### 4. Instalar dependências

```bash
pip install -r requirements.txt
```

Caso o arquivo `requirements.txt` ainda não esteja atualizado, instalar manualmente:

```bash
pip install fastapi uvicorn sqlalchemy psycopg2-binary python-dotenv
pip install email-validator
pip install "passlib[bcrypt]"
pip install "python-jose[cryptography]"
```

### 5. Atualizar `requirements.txt`

```bash
pip freeze > requirements.txt
```

---

## Variáveis de Ambiente

Criar o arquivo:

```text
backend/.env
```

Exemplo:

```env
DATABASE_URL=postgresql://postgres:SUA_SENHA@localhost:5432/techbridge_db
SECRET_KEY=techbridge_super_secret_key_change_later
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

Também é recomendado manter um arquivo de exemplo:

```text
backend/.env.example
```

Com:

```env
DATABASE_URL=postgresql://postgres:SUA_SENHA@localhost:5432/techbridge_db
SECRET_KEY=change_this_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

Importante: o arquivo `.env` não deve ser enviado para o GitHub.

---

## Como Rodar o Backend

Dentro da pasta `backend`, com o ambiente virtual ativado:

```bash
uvicorn app.main:app --reload
```

API local:

```text
http://127.0.0.1:8000
```

Documentação Swagger:

```text
http://127.0.0.1:8000/docs
```

---

## Como Rodar o Frontend

O frontend pode ser executado com a extensão **Live Server** do VS Code.

Passos:

1. Abrir o projeto no VS Code;
2. Instalar a extensão `Live Server`;
3. Clicar com botão direito em `frontend/index.html`;
4. Selecionar `Open with Live Server`.

URL esperada:

```text
http://127.0.0.1:5500/frontend/index.html
```

ou:

```text
http://127.0.0.1:5500/index.html
```

O backend precisa estar rodando em:

```text
http://127.0.0.1:8000
```

---

## CORS

O backend foi configurado para permitir chamadas do frontend local.

Origens permitidas:

```text
http://127.0.0.1:5500
http://localhost:5500
http://127.0.0.1:3000
http://localhost:3000
```

---

## Fluxo Principal do Sistema

```text
1. Empresa se cadastra
2. Empresa faz login
3. Sistema gera token JWT
4. Empresa cadastra resíduo
5. Outra empresa acessa o marketplace
6. Outra empresa demonstra interesse
7. Empresa dona do resíduo vê o interesse recebido
8. Empresa dona aceita ou rejeita o interesse
9. Se aceitar, o resíduo é reservado automaticamente
10. Empresa dona finaliza a negociação
11. Sistema marca o resíduo como vendido
12. Sistema cria uma transação
13. Dashboard e impacto ambiental são atualizados
```

---

## Roteiro de Demonstração

### 1. Cadastrar Empresa A

```json
{
  "company_name": "EcoMetal Industries",
  "email": "ecometal@test.com",
  "password": "123456",
  "city": "Palmas",
  "state": "TO",
  "industry": "Metallurgy"
}
```

### 2. Cadastrar Empresa B

```json
{
  "company_name": "GreenCycle Solutions",
  "email": "greencycle@test.com",
  "password": "123456",
  "city": "Guarulhos",
  "state": "SP",
  "industry": "Recycling"
}
```

### 3. Login com Empresa A

Acessar a tela de login e entrar com:

```json
{
  "email": "ecometal@test.com",
  "password": "123456"
}
```

### 4. Empresa A cadastra um resíduo

Tela:

```text
Meus resíduos
```

Exemplo:

```json
{
  "title": "Copper Wire Scrap",
  "description": "Copper wire leftovers from electrical production.",
  "material_type": "Copper",
  "quantity": 200,
  "unit": "kg",
  "city": "Palmas",
  "state": "TO"
}
```

### 5. Login com Empresa B

Sair da Empresa A e entrar com:

```json
{
  "email": "greencycle@test.com",
  "password": "123456"
}
```

### 6. Empresa B demonstra interesse

Tela:

```text
Marketplace
```

Ação:

```text
Clicar em "Tenho interesse"
```

### 7. Empresa A aceita o interesse

Sair da Empresa B e entrar novamente com a Empresa A.

Tela:

```text
Interesses
```

Ações:

```text
Aceitar interesse
Finalizar negociação
```

### 8. Conferir resultado

Telas para validar:

```text
Dashboard
Transações
Impacto ambiental
Marketplace
```

O resíduo finalizado deve deixar de aparecer como disponível no marketplace e passar a constar como transação concluída.

---

## Status Atual do Projeto

### Concluído

- Estrutura modular do backend;
- Conexão com PostgreSQL;
- Cadastro e login de empresas;
- Autenticação com JWT;
- Rotas protegidas;
- CRUD completo de resíduos;
- Marketplace com busca e filtros;
- Sistema de interesses entre empresas;
- Aceite, rejeição e cancelamento de interesses;
- Reserva automática de resíduos;
- Finalização de negociação;
- Registro de transações;
- Dashboard resumido;
- Estimativa inicial de impacto ambiental;
- Frontend com HTML, CSS e JavaScript;
- Landing page;
- Tela de cadastro;
- Tela de login;
- Tela de dashboard;
- Tela de marketplace;
- Tela de meus resíduos;
- Tela de interesses;
- Tela de transações.

### Próximos Passos

- Melhorar responsividade do frontend;
- Adicionar validação mais rigorosa de unidades de medida;
- Criar paginação no marketplace;
- Criar relatórios ambientais mais detalhados;
- Criar impacto ambiental por transação;
- Criar notificações;
- Criar deploy do backend e frontend;
- Melhorar segurança para ambiente de produção;
- Adicionar testes automatizados.

---

## Progresso Estimado

```text
Backend: 85% a 90%
Frontend MVP: 75% a 80%
Banco de dados: 80%
Autenticação: 90%
Marketplace core: 85%
Fluxo de negociação: 90%
Dashboard: 75%
Impacto ambiental: 60%
Documentação: 85%
Projeto geral: 80% a 85%
```

---

## `.gitignore` Recomendado

```gitignore
venv/
__pycache__/
.env
*.pyc
.pytest_cache/
.DS_Store
```

---

## Observações Técnicas

- Todo o código-fonte do backend foi escrito em inglês;
- As respostas técnicas da API estão em inglês;
- O frontend utiliza português na interface;
- O token JWT é armazenado no `localStorage`;
- Senhas são armazenadas apenas como hash;
- Rotas privadas dependem de autenticação;
- O backend utiliza arquitetura modular;
- O Swagger é usado para documentação e testes da API;
- O frontend consome a API usando `fetch`.

---

## Visão Futuro

O TechBridge / LoopIndustrial pode evoluir para uma plataforma SaaS B2B com:

- Matching inteligente entre empresas;
- Relatórios ambientais completos;
- Cálculo avançado de CO₂;
- Otimização logística;
- Gestão de contratos;
- Notificações;
- Upload de imagens dos resíduos;
- Painel administrativo;
- Deploy em nuvem;
- Integração com frontend moderno em React.