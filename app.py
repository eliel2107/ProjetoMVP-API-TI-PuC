from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError


from model import Session, Ativo, Manutencao 
from logger import logger

from schemas import (
    AtivoSchema, AtivoUpdateSchema, AtivoBuscaSchema, AtivoBuscaFiltroSchema,  # <-- ADICIONE AQUI
    AtivoViewSchema, ListagemAtivosSchema, AtivoDelSchema, ManutencaoSchema, 
    ErrorSchema, apresenta_ativo, apresenta_ativos
)
from flask_cors import CORS


info = Info(title="API de Estoque de TI", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)


home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
ativo_tag = Tag(name="Ativo", description="Adição, visualização, atualização e remoção de ativos de TI da base de dados")
manutencao_tag = Tag(name="Manutenção", description="Adição de um registro de manutenção a um ativo cadastrado")


@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')


@app.post('/ativo', tags=[ativo_tag],
          responses={"200": AtivoViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_ativo(form: AtivoSchema):
    """Adiciona um novo Ativo de TI à base de dados.

    Retorna uma representação do ativo e seus registros de manutenção associados.
    """
    ativo = Ativo(
        nome=form.nome,
        tipo=form.tipo, # Ex: Notebook, Monitor, Teclado
        tag_patrimonio=form.tag_patrimonio,
        status=form.status,
        valor_aquisicao=form.valor_aquisicao
    )
    logger.debug(f"Adicionando ativo com tag de patrimônio: '{ativo.tag_patrimonio}'")
    try:
        session = Session()
        session.add(ativo)
        session.commit()
        logger.debug(f"Adicionado ativo com tag: '{ativo.tag_patrimonio}'")
        return apresenta_ativo(ativo), 200

    except IntegrityError as e:
        error_msg = "Ativo com a mesma tag de patrimônio já salvo na base."
        logger.warning(f"Erro ao adicionar ativo '{ativo.nome}': {error_msg}")
        return {"message": error_msg}, 409

    except Exception as e:
        error_msg = "Não foi possível salvar novo ativo."
        logger.warning(f"Erro ao adicionar ativo '{ativo.nome}': {error_msg} - {e}")
        return {"message": error_msg}, 400


@app.get('/ativos', tags=[ativo_tag],
         responses={"200": ListagemAtivosSchema, "404": ErrorSchema})
def get_ativos(query: AtivoBuscaFiltroSchema):
    """Faz a busca por todos os Ativos de TI cadastrados na base,
       permitindo filtragem opcional por nome, tipo e status.

       Retorna uma representação da listagem de ativos.
    """
    logger.debug("Coletando ativos com base nos filtros")
    session = Session()

    
    db_query = session.query(Ativo)

    
    if query.nome:
        search = f"%{query.nome}%"
        db_query = db_query.filter(Ativo.nome.ilike(search))


    if query.tipo:
        search = f"%{query.tipo}%"
        db_query = db_query.filter(Ativo.tipo.ilike(search))


    if query.status:
        search = f"%{query.status}%"
        db_query = db_query.filter(Ativo.status.ilike(search))

    
    ativos = db_query.all()

    if not ativos:
        return {"ativos": []}, 200
    else:
        logger.debug(f"{len(ativos)} ativos encontrados")
        return apresenta_ativos(ativos), 200


@app.get('/ativo', tags=[ativo_tag],
         responses={"200": AtivoViewSchema, "404": ErrorSchema})
def get_ativo(query: AtivoBuscaSchema):
    """Faz a busca por um Ativo a partir da sua tag de patrimônio.

    Retorna uma representação do ativo e seus registros de manutenção.
    """
    tag_patrimonio = query.tag_patrimonio
    logger.debug(f"Coletando dados sobre o ativo #{tag_patrimonio}")
    session = Session()
    ativo = session.query(Ativo).filter(Ativo.tag_patrimonio == tag_patrimonio).first()

    if not ativo:
        error_msg = "Ativo não encontrado na base."
        logger.warning(f"Erro ao buscar ativo '{tag_patrimonio}': {error_msg}")
        return {"message": error_msg}, 404
    else:
        logger.debug(f"Ativo encontrado: '{ativo.nome}' (Tag: {ativo.tag_patrimonio})")
        return apresenta_ativo(ativo), 200


# =====================================================================
# NOVA ROTA PUT ADICIONADA AQUI
# =====================================================================
@app.put('/ativo', tags=[ativo_tag],
         responses={"200": AtivoViewSchema, "404": ErrorSchema})
def update_ativo(query: AtivoBuscaSchema, form: AtivoUpdateSchema):
    """Atualiza as informações de um Ativo de TI existente na base de dados.

    A busca pelo ativo a ser atualizado é feita pela tag de patrimônio.
    Apenas os campos informados no corpo da requisição serão atualizados.
    
    Retorna uma representação atualizada do ativo.
    """
    tag_patrimonio = query.tag_patrimonio
    logger.debug(f"Atualizando dados do ativo #{tag_patrimonio}")
    
    session = Session()
    ativo = session.query(Ativo).filter(Ativo.tag_patrimonio == tag_patrimonio).first()

    if not ativo:
        error_msg = "Ativo não encontrado na base."
        logger.warning(f"Erro ao atualizar ativo '{tag_patrimonio}', {error_msg}")
        return {"message": error_msg}, 404
    
    
    if form.nome:
        ativo.nome = form.nome
    if form.tipo:
        ativo.tipo = form.tipo
    if form.status: 
        ativo.status = form.status
    if form.valor_aquisicao:
        ativo.valor_aquisicao = form.valor_aquisicao
    
    session.commit()
    
    logger.debug(f"Ativo atualizado: '{ativo.tag_patrimonio}'")
    return apresenta_ativo(ativo), 200
# =====================================================================


@app.delete('/ativo', tags=[ativo_tag],
            responses={"200": AtivoDelSchema, "404": ErrorSchema})
def del_ativo(query: AtivoBuscaSchema):
    """Deleta um Ativo a partir da tag de patrimônio informada.

    Retorna uma mensagem de confirmação da remoção.
    """
    tag_patrimonio = query.tag_patrimonio
    logger.debug(f"Deletando dados sobre o ativo #{tag_patrimonio}")
    session = Session()
    count = session.query(Ativo).filter(Ativo.tag_patrimonio == tag_patrimonio).delete()
    session.commit()

    if count:
        logger.debug(f"Deletado ativo #{tag_patrimonio}")
        return {"message": "Ativo removido", "tag_patrimonio": tag_patrimonio}
    else:
        error_msg = "Ativo não encontrado na base."
        logger.warning(f"Erro ao deletar ativo '{tag_patrimonio}': {error_msg}")
        return {"message": error_msg}, 404


@app.post('/manutencao', tags=[manutencao_tag],
          responses={"200": AtivoViewSchema, "404": ErrorSchema})
def add_manutencao(form: ManutencaoSchema):
    """Adiciona um novo registro de manutenção a um ativo cadastrado na base.

    Retorna uma representação do ativo com seus registros de manutenção.
    """
    ativo_id = form.ativo_id
    logger.debug(f"Adicionando manutenção ao ativo de ID #{ativo_id}")
    session = Session()
    ativo = session.query(Ativo).filter(Ativo.id == ativo_id).first()

    if not ativo:
        error_msg = "Ativo não encontrado na base."
        logger.warning(f"Erro ao adicionar manutenção ao ativo '{ativo_id}': {error_msg}")
        return {"message": error_msg}, 404

   
    descricao = form.descricao
    manutencao = Manutencao(descricao)

    
    ativo.adiciona_manutencao(manutencao)
    session.commit()

    logger.debug(f"Adicionada manutenção ao ativo #{ativo_id}")
    return apresenta_ativo(ativo), 200