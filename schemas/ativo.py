from pydantic import BaseModel
from typing import Optional, List
<<<<<<< HEAD
from model.ativo import Ativo
from typing import Optional
=======
>>>>>>> 7de88b0 (Atualizações Finais do Back-End)
from schemas.manutencao import ManutencaoSchema


class AtivoSchema(BaseModel):
    """ Define como um novo ativo de TI a ser inserido deve ser representado.
    """
<<<<<<< HEAD
    nome: str = "Notebook Dell XPS 15"
    tipo: str = "Notebook"
    tag_patrimonio: str = "NTB-00124"
    status: Optional[str] = "Em estoque"
    valor_aquisicao: float = 9500.00


class AtivoBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca, que será
        feita com base na tag de patrimônio do ativo.
    """
    tag_patrimonio: str = "NTB-00124"

=======
    nome: str 
    tipo: str 
    tag_patrimonio: str 
    status: Optional[str] 
    valor_aquisicao: float 


class AtivoBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca.
    """
    tag_patrimonio: str

# ADICIONADO DE VOLTA: A classe que foi removida por engano
>>>>>>> 7de88b0 (Atualizações Finais do Back-End)
class AtivoBuscaFiltroSchema(BaseModel):
    """ Define a estrutura para a busca com filtros opcionais.
    """
    nome: Optional[str] = None
    tipo: Optional[str] = None
    status: Optional[str] = None


class ListagemAtivosSchema(BaseModel):
    """ Define como uma listagem de ativos será retornada.
    """
    ativos: List[AtivoSchema]


<<<<<<< HEAD
def apresenta_ativos(ativos: List[Ativo]):
    """ Retorna uma representação dos ativos seguindo o schema definido em
        AtivoViewSchema.
    """
    result = []
    for ativo in ativos:
        result.append({
            "id": ativo.id,
            "nome": ativo.nome,
            "tipo": ativo.tipo,
            "tag_patrimonio": ativo.tag_patrimonio,
            "status": ativo.status,
            "valor_aquisicao": ativo.valor_aquisicao,
        })

    return {"ativos": result}


class AtivoViewSchema(BaseModel):
    """ Define como um ativo será retornado: ativo + registros de manutenção.
    """
    id: int = 1
    nome: str = "Notebook Dell XPS 15"
    tipo: str = "Notebook"
    tag_patrimonio: str = "NTB-00124"
    status: str = "Em estoque"
    valor_aquisicao: float = 9500.00
    total_manutencoes: int = 1
=======
class AtivoViewSchema(BaseModel):
    """ Define como um ativo será retornado: ativo + registros de manutenção.
    """
    id: int 
    nome: str 
    tipo: str 
    tag_patrimonio: str 
    status: Optional[str] 
    valor_aquisicao: float 
    total_manutencoes: int 
>>>>>>> 7de88b0 (Atualizações Finais do Back-End)
    manutencoes: List[ManutencaoSchema]


class AtivoDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    message: str
    tag_patrimonio: str

class AtivoUpdateSchema(BaseModel):
    """ Define como os dados para atualização de um ativo serão representados.
        Todos os campos são opcionais.
    """
    nome: Optional[str] = None
    tipo: Optional[str] = None
    status: Optional[str] = None
    valor_aquisicao: Optional[float] = None

<<<<<<< HEAD

def apresenta_ativo(ativo: Ativo):
    """ Retorna uma representação do ativo seguindo o schema definido em
        AtivoViewSchema.
    """
    return {
        "id": ativo.id,
        "nome": ativo.nome,
        "tipo": ativo.tipo,
        "tag_patrimonio": ativo.tag_patrimonio,
        "status": ativo.status,
        "valor_aquisicao": ativo.valor_aquisicao,
        "total_manutencoes": len(ativo.manutencoes),
        "manutencoes": [{"descricao": m.descricao, "data_manutencao": m.data_manutencao} for m in ativo.manutencoes]
    }
=======
>>>>>>> 7de88b0 (Atualizações Finais do Back-End)
