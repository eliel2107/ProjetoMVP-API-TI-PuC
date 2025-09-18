🚀 API de Gestão de Ativos de TI - MVP PUC-Rio
API RESTful desenvolvida como parte do projeto MVP para a disciplina de Desenvolvimento Full Stack da PUC-Rio. A aplicação permite o gerenciamento completo de ativos de TI e seus respectivos registros de manutenção.

✨ Funcionalidades
A API oferece endpoints para realizar operações de CRUD (Criar, Ler, Atualizar, Deletar) para os seguintes recursos:

Ativos: Gerenciamento de equipamentos de TI, como notebooks, monitores, etc.

Manutenções: Gerenciamento do histórico de manutenções associadas a cada ativo.

🛠️ Tecnologias Utilizadas
Python 3.11+: Linguagem principal do projeto.

Flask: Micro-framework web para a construção da API.

Flask-OpenAPI3: Para a geração automática de documentação interativa (Swagger UI).

SQLAlchemy: ORM para a interação com o banco de dados.

Pydantic: Para validação de dados e definição de schemas.

SQLite: Banco de dados relacional leve utilizado no projeto.

⚙️ Como Executar o Projeto
Siga os passos abaixo para configurar e executar o servidor da API localmente.

Pré-requisitos
Python 3.11 ou superior instalado.

Git instalado.

Passos
Clone o repositório:

git clone <url_do_seu_repositorio_backend>
cd <nome_da_pasta_do_projeto>

Crie e ative um ambiente virtual:

No Windows:

python -m venv .venv
.\.venv\Scripts\activate

No macOS/Linux:

python3 -m venv .venv
source .venv/bin/activate

Instale as dependências:

pip install -r requirements.txt

Execute o servidor:

flask run

Por padrão, a API estará disponível em http://12.0.0.1:5000.

📚 Documentação da API (Swagger)
Com o servidor em execução, você pode acessar a documentação interativa da API (Swagger UI) para visualizar e testar todos os endpoints disponíveis:

http://127.0.0.1:5000/openapi/swagger
