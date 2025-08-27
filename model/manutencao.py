from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from datetime import datetime
from typing import Union

from .base import Base


class Manutencao(Base):
    __tablename__ = 'manutencao'

    id = Column(Integer, primary_key=True)
    descricao = Column(String(4000))
    data_manutencao = Column(DateTime, default=datetime.now())

    ativo_id = Column(Integer, ForeignKey("ativo.id"), nullable=False)

    def __init__(self, descricao:str, data_manutencao:Union[DateTime, None] = None):
        """
        Cria um Registro de Manutenção

        Arguments:
            descricao: A descrição do serviço ou ocorrência.
            data_manutencao: Data de quando a manutenção foi realizada ou inserida
                             na base.
        """
        self.descricao = descricao
        if data_manutencao:
            self.data_manutencao = data_manutencao