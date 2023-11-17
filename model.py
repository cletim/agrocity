from sqlalchemy import Column, String, Integer, Double
from database.connection import db

class Cliente(db.Model):
    __tablename__ = "cliente"

    idcliente = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String, nullable=False)
    email = Column(String, nullable=False)
    telefone = Column(String)
    cpf = Column(String)
    palestra = Column(String)
   