from sqlalchemy.orm import Session
from app.models.categoria import Categoria

def criar_categoria(db: Session, nome: str):
    nova_categoria = Categoria(nome=nome)
    db.add(nova_categoria)
    db.commit()
    db.refresh(nova_categoria)
    return nova_categoria
    
def listar_categorias(db: Session):
    return db.query(Categoria).all()

# Continue para atualizar e deletar
