from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

# Modelo Livro para o banco de dados
class Livro(Base):
    __tablename__ = "livros"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, index=True)
    autor = Column(String)
    ano = Column(Integer)
    genero = Column(String)
    categoria_id = Column(Integer, ForeignKey('categorias.id', ondelete='CASCADE'), nullable=True)  # Referência à tabela 'categorias' com CASCADE e nullable=True

    # Relacionamento com a tabela Categoria
    categoria = relationship("Categoria", back_populates="livros", cascade="all, delete")  # CASCADE para deletar livros associados quando a categoria for deletada

    # Campos de Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)  # Definido na criação
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # Atualizado automaticamente
