from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import os

from model.base import Base
from model.ativo import Ativo
from model.manutencao import Manutencao

db_path = "database/"
# Verifica se o diretorio não existe
if not os.path.exists(db_path):
   # então cria o diretorio
   os.makedirs(db_path)

# url de acesso ao banco (essa é uma url de acesso ao sqlite local)
db_url = 'sqlite:///%s/db.sqlite3' % db_path

# cria a engine de conexão com o banco
engine = create_engine(db_url, echo=False)

# Instancia um criador de seção com o banco
Session = sessionmaker(bind=engine)

# cria o banco se ele não existir 
if not database_exists(engine.url):
    create_database(engine.url) 

# cria as tabelas do banco, caso não existam
<<<<<<< HEAD
Base.metadata.create_all(engine)
=======
Base.metadata.create_all(engine)
def get_db():
    """
    Função 'Depends' que cria e fecha a sessão do banco.
    """
    db = Session() # 'Session' é a classe sessionmaker que você definiu acima 
    try:
        yield db
    finally:
        db.close()
>>>>>>> 7de88b0 (Atualizações Finais do Back-End)
