
# Projeto MVP - API TI PUC

API desenvolvida como parte do projeto MVP da disciplina de Arquitetura de Software da Pós-Graduação em Engenharia de Software da PUC-Rio.

## 🔧 Tecnologias Utilizadas

- **Python 3**
- **Flask**
- **SQLAlchemy**
- **SQLite**
- **Flask OpenAPI**
- **Flask CORS**
- **Pydantic**
- **JWT**
- **Bcrypt**
- **Docker** (opcional)

## 🚀 Como Executar

1. Clone o repositório:

   ```bash
   git clone https://github.com/eliel2107/ProjetoMVP-API-TI-PuC.git
   cd ProjetoMVP-API-TI-PuC
   ```

2. Crie e ative um ambiente virtual:

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # No Windows use: venv\Scripts\activate
   ```

3. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

4. Execute a aplicação:

   ```bash
   flask run --host 0.0.0.0 --port 5000
   ```

5. Acesse a documentação da API em [http://localhost:5000/openapi/swagger](http://localhost:5000/openapi/swagger).

## 🗂 Estrutura do Projeto

```plaintext
ProjetoMVP-API-TI-PuC/
├── app.py             # Arquivo principal da aplicação
├── logger.py          # Configuração de logs
├── requirements.txt   # Dependências do projeto
├── model/             # Modelos de dados e lógica de negócios
│   ├── __init__.py
│   ├── base.py
│   ├── email_client.py
│   ├── email.py
│   └── reminder.py
├── schemas/           # Schemas de validação e resposta
│   ├── __init__.py
│   ├── error.py
│   └── reminder.py
└── .gitignore         # Arquivos a serem ignorados pelo Git
```

## 🧪 Testes

Para executar os testes, utilize o comando:

```bash
pytest
```

## 📄 Licença

Este projeto está licenciado sob a licença MIT.
