
# Sistema de Controle de Ferramentas

Sistema web desenvolvido como MVP para gerenciar ferramentas e equipamentos utilizados por uma equipe de serviços de campo.

## Objetivo

Centralizar o controle de ferramentas, permitindo consultar a disponibilidade dos equipamentos e registrar retiradas e devoluções, mantendo um histórico das movimentações.

## Funcionalidades

- Consulta de ferramentas por patrimônio ou descrição.
- Visualização da disponibilidade dos equipamentos.
- Registro de retirada com identificação do colaborador responsável.
- Registro de devolução.
- Atualização automática da disponibilidade.
- Histórico de movimentações.
- Validação para impedir retiradas duplicadas e devoluções inválidas.

## Tecnologias utilizadas

- Python 3
- Flask
- Flask-SQLAlchemy
- SQLAlchemy
- MySQL Connector/Python
- Bootstrap 5
- Pytest
- Git e GitHub
- GitHub Actions

## Estrutura do projeto

```text
ControleFerramentas/
├── app/
│   ├── static/
│   │   └── css/
│   ├── templates/
│   │   ├── base.html
│   │   ├── ferramentas.html
│   │   └── movimentacoes.html
│   ├── __init__.py
│   ├── models.py
│   └── routes.py
├── tests/
│   ├── conftest.py
│   └── test_movimentacoes.py
├── .github/
│   └── workflows/
│       └── ci.yml
├── config.py
├── requirements.txt
├── run.py
└── README.md
```

## Instalação e execução

### 1. Clonar o repositório

```bash
git clone https://github.com/MatheusFerrei-ra/controle-ferramentas.git
cd controle-ferramentas
```

### 2. Criar o ambiente virtual

```bash
python3 -m venv venv
```

### 3. Ativar o ambiente virtual

macOS e Linux:

```bash
source venv/bin/activate
```

### 4. Instalar as dependências

```bash
pip install -r requirements.txt
```

### 5. Executar a aplicação

```bash
python run.py
```

A aplicação estará disponível em:

http://127.0.0.1:5000

## Testes automatizados

Para executar os testes:

```bash
python -m pytest -v
```

Os testes verificam:

- A abertura da página inicial.
- A consulta de ferramentas.
- O registro de retirada.
- O bloqueio de retirada duplicada.
- O registro de devolução.

## Integração contínua

O projeto utiliza GitHub Actions para executar automaticamente os testes automatizados em eventos de envio de código e Pull Requests direcionados à branch principal.

## Banco de dados

A aplicação utiliza Flask-SQLAlchemy para o mapeamento das entidades:

- Ferramenta
- Colaborador
- Movimentação

A configuração do banco de dados é definida no arquivo `config.py`.

## Observação

Este projeto corresponde a um MVP acadêmico. Os registros iniciais utilizados na demonstração são fictícios.
