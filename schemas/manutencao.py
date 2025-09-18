from pydantic import BaseModel
<<<<<<< HEAD

=======
from typing import Optional
from datetime import datetime
>>>>>>> 7de88b0 (Atualizações Finais do Back-End)

class ManutencaoSchema(BaseModel):
    """ Define como um novo registro de manutenção a ser inserido deve ser representado.
    """
<<<<<<< HEAD
    ativo_id: int = 1
    descricao: str = "Troca de HD por um SSD de 512GB."
=======
    ativo_id: int
    descricao: str


class ManutencaoBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca, que será
        feita com base no ID da manutenção.
    """
    id: int


class ManutencaoUpdateSchema(BaseModel):
    """ Define como os dados para atualização de uma manutenção serão representados.
    """
    descricao: str

# ADICIONADO: Schema para a resposta da rota de deleção
class ManutencaoDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção de manutenção.
    """
    message: str
    id: int

>>>>>>> 7de88b0 (Atualizações Finais do Back-End)
