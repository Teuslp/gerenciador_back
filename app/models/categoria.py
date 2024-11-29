from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base
from pydantic import BaseModel

# Modelo SQLAlchemy para a tabela 'categorias'
class Categoria(Base):
    __tablename__ = "categorias"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, unique=True, index=True)

    # Relacionamento reverso com Livro (a tabela 'livros' possui a chave estrangeira categoria_id)
    livros = relationship("Livro", back_populates="categoria")

# Classe Pydantic para criação de categoria
class CategoriaCreate(BaseModel):
    nome: str

    class Config:
        orm_mode = True  # Permite que o Pydantic use objetos do SQLAlchemy diretamente

# Classe Pydantic para a resposta (saída de dados)
class CategoriaResponse(BaseModel):
    id: int
    nome: str

    class Config:
        orm_mode = True  # Permite que o Pydantic use objetos do SQLAlchemy diretamente
        from_attributes = True  # Permite o uso de from_orm

# Classe CategoriaOut para saída de dados (caso você precise retornar o id também)
class CategoriaOut(BaseModel):
    id: int
    nome: str

    class Config:
        orm_mode = True  # Permite que o Pydantic use objetos do SQLAlchemy diretamente
