from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.livro import Livro
from app.database import engine, Base, get_db
from app.models import user, livro
from app.models.user import Usuario
from passlib.context import CryptContext
from dotenv import load_dotenv
from jose import JWTError, jwt
from datetime import datetime, timedelta
from app.utils.auth import get_current_user
from pydantic import BaseModel
import os

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Bem-vindo à API de Gerenciamento de Livros!"}


# Criação das tabelas no banco
Base.metadata.create_all(bind=engine)

# Criar um novo livro (Apenas usuários autenticados)
@app.post("/livros/", status_code=201)
def criar_livro(
    titulo: str,
    autor: str,
    ano: int,
    genero: str,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),  # Novo parâmetro
):
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
def atualizar_livro(livro_id: int, titulo: str, autor: str, ano: int, genero: str, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
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
def deletar_livro(livro_id: int, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    livro = db.query(Livro).filter(Livro.id == livro_id).first()
    if not livro:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    db.delete(livro)
    db.commit()
    return {"message": "Livro deletado com sucesso"}


# Carrega as variáveis do arquivo .env
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@app.post("/register")
def register(nome_usuario: str, senha: str, db: Session = Depends(get_db)):
    hashed_senha = pwd_context.hash(senha)
    novo_usuario = Usuario(nome_usuario=nome_usuario, senha_hash=hashed_senha)
    
    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)
    return {"message": "Usuário registrado com sucesso", "user": novo_usuario.nome_usuario}


# Pegar essas variáveis do .env
SECRET_KEY = "sua_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


   # Criar um modelo para os dados de login
class LoginData(BaseModel):
    nome_usuario: str
    senha: str 

@app.post("/login")
def login(data: LoginData, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.nome_usuario == data.nome_usuario).first()
    
    if not usuario or not pwd_context.verify(data.senha, usuario.senha_hash):
        raise HTTPException(status_code=401, detail="Credenciais inválidas")

    access_token = create_access_token(data={"sub": usuario.nome_usuario})
    return {"access_token": access_token, "token_type": "bearer"}