from sqlalchemy.orm import Session
from app.models.user import Usuario

def criar_usuario(db: Session, nome_usuario: str, senha_hash: str):
    novo_usuario = Usuario(nome_usuario=nome_usuario, senha_hash=senha_hash)
    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)
    return novo_usuario

def buscar_usuario_por_nome(db: Session, nome_usuario: str):
    return db.query(Usuario).filter(Usuario.nome_usuario == nome_usuario).first()
