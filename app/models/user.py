from sqlalchemy import Column, Integer, String
from app.database import Base

class Usuario(Base):
    __tablename__ = "usuarios"  # Nome da tabela no banco de dados

    id = Column(Integer, primary_key=True, index=True)  # ID do usuário (chave primária)
    nome_usuario = Column(String, unique=True, index=True, nullable=False)  # Nome de login (único)
    senha_hash = Column(String, nullable=False)  # Senha criptografada
