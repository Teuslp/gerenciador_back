from sqlalchemy import Column, Integer, String
from app.database import Base

# Modelo Livro para o banco de dados
class Livro(Base):
    __tablename__ = "livros"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, index=True)
    autor = Column(String, index=True)
    ano = Column(Integer)
    genero = Column(String)
