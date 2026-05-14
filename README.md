# TechBridge / LoopIndustrial

## Visão Geral do Projeto

O **TechBridge / LoopIndustrial** é uma plataforma digital B2B voltada para indústria inteligente e economia circular.

O principal objetivo da plataforma é conectar empresas que geram resíduos industriais com empresas que podem reutilizar esses materiais como matéria-prima.

A proposta do projeto é transformar o descarte industrial, que normalmente gera custo, em uma nova oportunidade de negócio, unindo sustentabilidade, eficiência operacional e vantagem competitiva.

---

## Conceito Principal

Muitos resíduos industriais com potencial de reaproveitamento acabam sendo descartados porque as empresas não estão conectadas entre si.

O sistema resolve esse problema atuando como uma ponte entre:

- Empresas que geram resíduos industriais;
- Empresas que precisam de matéria-prima alternativa;
- Necessidades de sustentabilidade;
- Controle de impacto ambiental;
- Conformidade com normas e relatórios regulatórios.

---

## Funcionalidades Planejadas

A plataforma está planejada para conter:

- Marketplace B2B industrial;
- Cadastro de empresas;
- Cadastro de resíduos industriais;
- Conexão inteligente entre empresas;
- Dashboard ambiental;
- Cálculo de redução de CO₂;
- Relatórios regulatórios;
- Rastreabilidade de materiais;
- Otimização logística;
- Autenticação segura com JWT.

---

## Tecnologias Utilizadas

### Backend

- Python;
- FastAPI;
- SQLAlchemy;
- PostgreSQL;
- Pydantic;
- JWT Authentication;
- Passlib com bcrypt;
- Python Dotenv.

### Frontend

Versão inicial:

- HTML;
- CSS;
- JavaScript.

Possível evolução futura:

- React.

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
│   │   │   ├── hashing.py
│   │   │   └── jwt_handler.py
│   │   │
│   │   ├── database/
│   │   │   ├── base.py
│   │   │   └── db.py
│   │   │
│   │   ├── models/
│   │   │   └── company.py
│   │   │
│   │   ├── routes/
│   │   │   └── company_routes.py
│   │   │
│   │   ├── schemas/
│   │   │   └── company_schema.py
│   │   │
│   │   ├── services/
│   │   │
│   │   └── main.py
│   │
│   ├── .env
│   └── requirements.txt
│
├── frontend/
│   ├── assets/
│   ├── css/
│   ├── js/
│   └── pages/
│
└── README.md