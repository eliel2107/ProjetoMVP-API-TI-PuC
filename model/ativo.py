from sqlalchemy import Column, String, Integer, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union

from .base import Base
from .manutencao import Manutencao


class Ativo(Base):
    __tablename__ = 'ativo'

    id = Column(Integer, primary_key=True)
    nome = Column(String(140))
    tipo = Column(String(140)) # Ex: Notebook, Monitor, Teclado
    tag_patrimonio = Column(String(140), unique=True)
    status = Column(String(140), default="Em Estoque") # Ex: Ativo, Inativo, Manutenção
    valor_aquisicao = Column(Float)
    data_insercao = Column(DateTime, default=datetime.now())

    manutencoes = relationship("Manutencao")

    # O método __init__ foi atualizado para incluir o 'status'
    def __init__(self, nome:str, tipo:str, tag_patrimonio:str, valor_aquisicao:float,
                 status:str,  # <-- MUDANÇA AQUI (1/2)
                 data_insercao:Union[DateTime, None] = None):
        """
        Cria um Ativo de TI

        Arguments:
            nome: Nome ou descrição do ativo.
            tipo: Categoria do ativo.
            tag_patrimonio: Etiqueta de patrimônio única do ativo.
            valor_aquisicao: Custo de aquisição do ativo.
            status: O estado atual do ativo (ex: "Em estoque").
            data_insercao: Data de quando o ativo foi inserido na base.
        """
        self.nome = nome
        self.tipo = tipo
        self.tag_patrimonio = tag_patrimonio
        self.valor_aquisicao = valor_aquisicao
        self.status = status  # <-- MUDANÇA AQUI (2/2)

        if data_insercao:
            self.data_insercao = data_insercao

    def adiciona_manutencao(self, manutencao:Manutencao):
        """ Adiciona um novo registro de manutenção ao Ativo
        """
        self.manutencoes.append(manutencao)