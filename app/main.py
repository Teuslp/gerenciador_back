from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.livro import Livro
from app.database import engine, Base, get_db
from app.models import user, livro

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Bem-vindo à API de Gerenciamento de Livros!"}


# Criação das tabelas no banco
Base.metadata.create_all(bind=engine)

# Criar um novo livro
@app.post("/livros/", status_code=201)
def criar_livro(titulo: str, autor: str, ano: int, genero: str, db: Session = Depends(get_db)):
    novo_livro = Livro(titulo=titulo, autor=autor, ano=ano, genero=genero)
    db.add(novo_livro)
    db.commit()
    db.refresh(novo_livro)
    return novo_livro

# Listar todos os livros
@app.get("/livros/")
def listar_livros(db: Session = Depends(get_db)):
    return db.query(Livro).all()

# Buscar um livro por ID
@app.get("/livros/{livro_id}")
def buscar_livro(livro_id: int, db: Session = Depends(get_db)):
    livro = db.query(Livro).filter(Livro.id == livro_id).first()
    if not livro:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    return livro

# Atualizar um livro
@app.put("/livros/{livro_id}")
def atualizar_livro(livro_id: int, titulo: str, autor: str, ano: int, genero: str, db: Session = Depends(get_db)):
    livro = db.query(Livro).filter(Livro.id == livro_id).first()
    if not livro:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    livro.titulo = titulo
    livro.autor = autor
    livro.ano = ano
    livro.genero = genero
    db.commit()
    db.refresh(livro)
    return livro

# Deletar um livro
@app.delete("/livros/{livro_id}")
def deletar_livro(livro_id: int, db: Session = Depends(get_db)):
    livro = db.query(Livro).filter(Livro.id == livro_id).first()
    if not livro:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    db.delete(livro)
    db.commit()
    return {"message": "Livro deletado com sucesso"}

