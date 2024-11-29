from app.models.categoria import Categoria as CategoriaModel
from sqlalchemy.orm import Session
from app.schemas.categoria import CategoriaCreate

def criar_categoria_service(db: Session, nome: str):
    categoria = CategoriaModel(nome=nome)
    db.add(categoria)
    db.commit()
    db.refresh(categoria)
    return categoria  # Retorna o objeto SQLAlchemy

def listar_categorias_service(db: Session):
    categorias = db.query(CategoriaModel).all()
    return categorias  # Retorna uma lista de objetos SQLAlchemy
