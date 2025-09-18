from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote

from flask import request
from model import Session
from sqlalchemy.exc import IntegrityError

from model import Ativo, Manutencao 
from logger import logger

from schemas import (
    AtivoSchema, AtivoUpdateSchema, AtivoBuscaSchema, AtivoBuscaFiltroSchema,
    AtivoViewSchema, ListagemAtivosSchema, AtivoDelSchema, 
    ManutencaoSchema, ManutencaoBuscaSchema, ManutencaoUpdateSchema, ManutencaoDelSchema,
    ErrorSchema, apresenta_ativo, apresenta_ativos
)
from flask_cors import CORS

# Imports necessários para o comando init-db
from model import engine
from model.base import Base


info = Info(title="API de Gestão de Ativos de TI", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# --- COMANDO CLI PARA INICIALIZAR O BANCO DE DADOS ---
@app.cli.command("init-db")
def init_db_command():
    """Cria as tabelas do banco de dados a partir dos modelos."""
    print("Iniciando a criação das tabelas no banco de dados...")
    # O comando Base.metadata.create_all() usa a 'engine' para criar
    # todas as tabelas que herdam de 'Base' (Ativo e Manutencao).
    Base.metadata.create_all(engine)
    print("Tabelas 'ativo' e 'manutencao' criadas com sucesso.")


# --- DEFINIÇÃO DAS TAGS PARA O SWAGGER ---
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
ativo_tag = Tag(name="Ativo", description="Adição, visualização, atualização e remoção de ativos de TI da base de dados")
manutencao_tag = Tag(name="Manutenção", description="Adição, visualização, atualização e remoção de registros de manutenção")


@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação."""
    return redirect('/openapi')


# --- ROTAS DE ATIVO ---

@app.post('/ativo', tags=[ativo_tag],
          responses={"200": AtivoViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_ativo():
    """Adiciona um novo Ativo de TI à base de dados."""
    try:
        data = request.get_json()
        if not data:
            return {"message": "Corpo (body) da requisição está vazio ou não é JSON."}, 400
        ativo_schema = AtivoSchema(**data) 
    except Exception as e:
        logger.warning(f"Erro de validação ao adicionar ativo: {e}")
        return {"message": "Erro de validação nos dados enviados", "details": str(e)}, 400
    
    with Session() as db:
        try:
            ativo = Ativo(
                tag_patrimonio=ativo_schema.tag_patrimonio,
                nome=ativo_schema.nome,
                tipo=ativo_schema.tipo,
                status=ativo_schema.status,
                valor_aquisicao=ativo_schema.valor_aquisicao
            )
            db.add(ativo)
            db.commit()
            db.refresh(ativo) 
            logger.debug(f"Adicionado ativo com tag: '{ativo.tag_patrimonio}'")
            return apresenta_ativo(ativo), 200
        except IntegrityError:
            db.rollback() 
            error_msg = "Ativo com a mesma tag de patrimônio já salvo na base."
            logger.warning(f"Erro ao adicionar ativo '{ativo_schema.nome}': {error_msg}")
            return {"message": error_msg}, 409
        except Exception as e:
            db.rollback() 
            error_msg = "Não foi possível salvar novo ativo."
            logger.warning(f"Erro ao adicionar ativo '{ativo_schema.nome}': {error_msg} - {e}")
            return {"message": error_msg}, 400

@app.get('/ativos', tags=[ativo_tag],
         responses={"200": ListagemAtivosSchema, "404": ErrorSchema})
def get_ativos():
    """Faz a busca por todos os Ativos de TI, permitindo filtragem opcional."""
    logger.debug("Coletando ativos com base nos filtros")
    
    with Session() as db:
        db_query = db.query(Ativo)
        
        nome_filtro = request.args.get('nome')
        tipo_filtro = request.args.get('tipo')
        status_filtro = request.args.get('status')

        if nome_filtro:
            search = f"%{nome_filtro}%"
            db_query = db_query.filter(Ativo.nome.ilike(search))
        if tipo_filtro:
            search = f"%{tipo_filtro}%"
            db_query = db_query.filter(Ativo.tipo.ilike(search))
        if status_filtro:
            search = f"%{status_filtro}%"
            db_query = db_query.filter(Ativo.status.ilike(search))

        ativos = db_query.all()
        
        if not ativos:
            return {"ativos": []}, 200
        else:
            logger.debug(f"{len(ativos)} ativos encontrados")
            return apresenta_ativos(ativos), 200

@app.get('/ativo', tags=[ativo_tag],
         responses={"200": AtivoViewSchema, "404": ErrorSchema})
def get_ativo():
    """Faz a busca por um Ativo a partir da sua tag de patrimônio."""
    tag_patrimonio = request.args.get('tag_patrimonio')
    if not tag_patrimonio:
        return {"message": "Parâmetro 'tag_patrimonio' é obrigatório."}, 400
    
    logger.debug(f"Coletando dados sobre o ativo #{tag_patrimonio}")
    with Session() as db:
        ativo = db.query(Ativo).filter(Ativo.tag_patrimonio == tag_patrimonio).first()
        if not ativo:
            error_msg = "Ativo não encontrado na base."
            logger.warning(f"Erro ao buscar ativo '{tag_patrimonio}': {error_msg}")
            return {"message": error_msg}, 404
        else:
            logger.debug(f"Ativo encontrado: '{ativo.nome}'")
            return apresenta_ativo(ativo), 200

@app.put('/ativo', tags=[ativo_tag],
         responses={"200": AtivoViewSchema, "404": ErrorSchema, "400": ErrorSchema})
def update_ativo():
    """Atualiza as informações de um Ativo de TI."""
    tag_patrimonio = request.args.get('tag_patrimonio')
    if not tag_patrimonio:
        return {"message": "Parâmetro 'tag_patrimonio' é obrigatório."}, 400
    
    try:
        data = request.get_json()
        update_data = AtivoUpdateSchema(**data)
    except Exception as e:
        return {"message": "Erro de validação nos dados enviados", "details": str(e)}, 400

    logger.debug(f"Atualizando dados do ativo #{tag_patrimonio}")
    with Session() as db:
        ativo = db.query(Ativo).filter(Ativo.tag_patrimonio == tag_patrimonio).first()
        if not ativo:
            error_msg = "Ativo não encontrado na base."
            logger.warning(f"Erro ao atualizar ativo '{tag_patrimonio}', {error_msg}")
            return {"message": error_msg}, 404
        
        if update_data.nome: ativo.nome = update_data.nome
        if update_data.tipo: ativo.tipo = update_data.tipo
        if update_data.status: ativo.status = update_data.status
        if update_data.valor_aquisicao is not None: ativo.valor_aquisicao = update_data.valor_aquisicao
        
        db.commit()
        logger.debug(f"Ativo atualizado: '{ativo.tag_patrimonio}'")
        return apresenta_ativo(ativo), 200

@app.delete('/ativo', tags=[ativo_tag],
            responses={"200": AtivoDelSchema, "404": ErrorSchema})
def del_ativo():
    """Deleta um Ativo a partir da tag de patrimônio informada."""
    tag_patrimonio = request.args.get('tag_patrimonio')
    if not tag_patrimonio:
        return {"message": "Parâmetro 'tag_patrimonio' é obrigatório."}, 400

    logger.debug(f"Deletando dados sobre o ativo #{tag_patrimonio}")
    with Session() as db:
        count = db.query(Ativo).filter(Ativo.tag_patrimonio == tag_patrimonio).delete()
        db.commit()
        if count:
            logger.debug(f"Deletado ativo #{tag_patrimonio}")
            return {"message": "Ativo removido", "tag_patrimonio": tag_patrimonio}
        else:
            error_msg = "Ativo não encontrado na base."
            logger.warning(f"Erro ao deletar ativo '{tag_patrimonio}': {error_msg}")
            return {"message": error_msg}, 404

# --- ROTAS DE MANUTENÇÃO ---

@app.post('/manutencao', tags=[manutencao_tag],
          responses={"200": AtivoViewSchema, "404": ErrorSchema, "400": ErrorSchema})
def add_manutencao():
    """Adiciona um novo registro de manutenção a um ativo cadastrado na base."""
    try:
        data = request.get_json()
        manutencao_schema = ManutencaoSchema(**data)
    except Exception as e:
        return {"message": "Erro de validação nos dados enviados", "details": str(e)}, 400

    ativo_id = manutencao_schema.ativo_id
    logger.debug(f"Adicionando manutenção ao ativo de ID #{ativo_id}")
    with Session() as db:
        ativo = db.query(Ativo).filter(Ativo.id == ativo_id).first()
        if not ativo:
            error_msg = "Ativo não encontrado na base."
            logger.warning(f"Erro ao adicionar manutenção ao ativo '{ativo_id}': {error_msg}")
            return {"message": error_msg}, 404
        
        manutencao = Manutencao(descricao=manutencao_schema.descricao)
        ativo.adiciona_manutencao(manutencao)
        db.commit()
        logger.debug(f"Adicionada manutenção ao ativo #{ativo_id}")
        return apresenta_ativo(ativo), 200

@app.delete('/manutencao', tags=[manutencao_tag],
            responses={"200": ManutencaoDelSchema, "404": ErrorSchema})
def del_manutencao():
    """Deleta uma manutenção a partir do seu id."""
    manutencao_id = request.args.get('id')
    if not manutencao_id:
        return {"message": "Parâmetro 'id' da manutenção é obrigatório."}, 400
    
    logger.debug(f"Deletando manutenção #{manutencao_id}")
    with Session() as db:
        count = db.query(Manutencao).filter(Manutencao.id == manutencao_id).delete()
        db.commit()
        if count:
            logger.debug(f"Deletada manutenção #{manutencao_id}")
            return {"message": "Manutenção removida", "id": int(manutencao_id)}
        else:
            error_msg = "Manutenção não encontrada na base."
            logger.warning(f"Erro ao deletar manutenção '{manutencao_id}': {error_msg}")
            return {"message": error_msg}, 404

@app.put('/manutencao', tags=[manutencao_tag],
         responses={"200": AtivoViewSchema, "404": ErrorSchema, "400": ErrorSchema})
def update_manutencao():
    """Atualiza a descrição de uma manutenção."""
    manutencao_id = request.args.get('id')
    if not manutencao_id:
        return {"message": "Parâmetro 'id' da manutenção é obrigatório."}, 400

    try:
        data = request.get_json()
        update_data = ManutencaoUpdateSchema(**data)
    except Exception as e:
        return {"message": "Erro de validação nos dados enviados", "details": str(e)}, 400
    
    logger.debug(f"Atualizando manutenção #{manutencao_id}")
    with Session() as db:
        manutencao = db.query(Manutencao).filter(Manutencao.id == manutencao_id).first()
        if not manutencao:
            error_msg = "Manutenção não encontrada na base."
            logger.warning(f"Erro ao atualizar manutenção '{manutencao_id}': {error_msg}")
            return {"message": error_msg}, 404
        
        manutencao.descricao = update_data.descricao
        db.commit()
        logger.debug(f"Atualizada manutenção #{manutencao_id}")
        return apresenta_ativo(manutencao.ativo)

