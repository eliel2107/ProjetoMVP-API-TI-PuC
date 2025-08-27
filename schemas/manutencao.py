from pydantic import BaseModel


class ManutencaoSchema(BaseModel):
    """ Define como um novo registro de manutenção a ser inserido deve ser representado.
    """
    ativo_id: int = 1
    descricao: str = "Troca de HD por um SSD de 512GB."