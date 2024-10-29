# Bibliotecas

Este projeto utiliza várias bibliotecas Python para gerenciar autenticação, hashing de senhas, manipulação de dados e construção de uma API rápida e eficiente. Para instalar todas as dependências, execute o comando abaixo:

### Instalação das Bibliotecas

```bash
pip install python-multipart pyjwt "passlib[bcrypt]" fastapi uvicorn sqlalchemy psycopg2-binary
```

### Descrição das Bibliotecas

- **Multipart**: Suporte para trabalhar com dados `multipart/form-data`.
- **PyJWT**: Biblioteca para manipular JSON Web Tokens (JWT), usada para autenticação.
- **Passlib com Bcrypt**: Biblioteca para hashing de senhas de forma segura com suporte a bcrypt.
- **FastAPI**: Framework web moderno e de alto desempenho para construção de APIs com Python.
- **Uvicorn**: Servidor ASGI de alto desempenho, ideal para rodar aplicações FastAPI.
- **SQLAlchemy**: ORM (Object-Relational Mapper) para facilitar o trabalho com bancos de dados relacionais em Python.
- **Psycopg2-binary**: Adaptador de banco de dados PostgreSQL para Python.

# Executando o Projeto

Após instalar as dependências, você pode executar a aplicação com o servidor uvicorn:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```