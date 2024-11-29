import logging
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.models.livro import Livro
from app.database import engine, Base, get_db
from app.models.user import Usuario
from pydantic import BaseModel
from app.utils.auth import pwd_context, criar_acesso_token, get_current_user
import os
import jwt
from dotenv import load_dotenv
from app.models.categoria import Categoria
from app.services.categoria_service import criar_categoria_service, listar_categorias_service
from typing import List
from app.models.categoria import CategoriaResponse  # Importar o modelo Pydantic de resposta


# Carregar variáveis de ambiente
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

# Configuração do logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# OAuth2PasswordBearer cria a dependência para pegar o token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Dependência para verificar o JWT
def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        # Decodifica o token JWT
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return username
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

# Criação das tabelas no banco
Base.metadata.create_all(bind=engine)

# -------------------------------------------
# Endpoints de Livros
# -------------------------------------------

@app.get("/")
def read_root():
    return {"message": "Bem-vindo à API de Gerenciamento de Livros!"}

@app.post("/livros/", status_code=201)
def criar_livro(
    titulo: str,
    autor: str,
    ano: int,
    genero: str,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(verify_token),  # Protege o endpoint com a dependência do JWT
):
    novo_livro = Livro(titulo=titulo, autor=autor, ano=ano, genero=genero)
    db.add(novo_livro)
    db.commit()
    db.refresh(novo_livro)
    logger.info(f"Livro '{titulo}' criado por {current_user}")  # Log de sucesso
    return novo_livro

@app.get("/livros/")
def listar_livros(db: Session = Depends(get_db)):
    livros = db.query(Livro).all()  # Já trará created_at e updated_at
    logger.info(f"Listando {len(livros)} livros.")  # Log de listagem de livros
    return livros

@app.get("/livros/{livro_id}")
def buscar_livro(livro_id: int, db: Session = Depends(get_db)):
    livro = db.query(Livro).filter(Livro.id == livro_id).first()
    if not livro:
        logger.warning(f"Livro com ID {livro_id} não encontrado.")  # Log de erro
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    logger.info(f"Livro com ID {livro_id} encontrado: {livro.titulo}")  # Log de sucesso
    return livro

@app.put("/livros/{livro_id}")
def atualizar_livro(livro_id: int, titulo: str, autor: str, ano: int, genero: str, db: Session = Depends(get_db), current_user: Usuario = Depends(verify_token)):
    livro = db.query(Livro).filter(Livro.id == livro_id).first()
    if not livro:
        logger.warning(f"Livro com ID {livro_id} não encontrado para atualização.")  # Log de erro
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    
    livro.titulo = titulo
    livro.autor = autor
    livro.ano = ano
    livro.genero = genero
    db.commit()
    db.refresh(livro)
    logger.info(f"Livro com ID {livro_id} atualizado por {current_user}")  # Log de sucesso
    return livro

@app.delete("/livros/{livro_id}")
def deletar_livro(livro_id: int, db: Session = Depends(get_db), current_user: Usuario = Depends(verify_token)):
    livro = db.query(Livro).filter(Livro.id == livro_id).first()
    if not livro:
        logger.warning(f"Tentativa de exclusão de livro com ID {livro_id}, mas livro não encontrado.")  # Log de erro
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    db.delete(livro)
    db.commit()
    logger.info(f"Livro com ID {livro_id} deletado por {current_user}")  # Log de sucesso
    return {"message": "Livro deletado com sucesso"}

# -------------------------------------------
# Endpoints de Categorias
# -------------------------------------------

@app.post("/categorias/", response_model=CategoriaResponse)
def criar_categoria(nome: str, db: Session = Depends(get_db)):
    categoria = Categoria(nome=nome)  # O 'id' será gerado automaticamente
    db.add(categoria)
    db.commit()
    db.refresh(categoria)  # Atualiza a categoria para incluir o 'id'
    logger.info(f"Categoria '{nome}' criada.")  # Log de sucesso
    return CategoriaResponse.from_orm(categoria)  # Retorna o modelo Pydantic CategoriaResponse

@app.get("/categorias/", response_model=List[CategoriaResponse])
def listar_categorias(db: Session = Depends(get_db)):
    categorias = listar_categorias_service(db)
    logger.info(f"Listando {len(categorias)} categorias.")  # Log de listagem de categorias
    return [CategoriaResponse.from_orm(categoria) for categoria in categorias]


@app.put("/categorias/{categoria_id}", response_model=CategoriaResponse)
def atualizar_categoria(categoria_id: int, nome: str, db: Session = Depends(get_db)):
    categoria = db.query(Categoria).filter(Categoria.id == categoria_id).first()
    if not categoria:
        logger.warning(f"Categoria com ID {categoria_id} não encontrada para atualização.")  # Log de erro
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    
    categoria.nome = nome
    db.commit()
    db.refresh(categoria)
    logger.info(f"Categoria com ID {categoria_id} atualizada para '{nome}'.")  # Log de sucesso
    return CategoriaResponse.from_orm(categoria)  # Retorna o modelo Pydantic CategoriaResponse


@app.delete("/categorias/{categoria_id}")
def deletar_categoria(categoria_id: int, db: Session = Depends(get_db)):
    categoria = db.query(Categoria).filter(Categoria.id == categoria_id).first()
    if not categoria:
        logger.warning(f"Tentativa de exclusão de categoria com ID {categoria_id}, mas categoria não encontrada.")  # Log de erro
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    db.delete(categoria)
    db.commit()
    logger.info(f"Categoria com ID {categoria_id} deletada.")  # Log de sucesso
    return {"message": "Categoria deletada com sucesso"}

# -------------------------------------------
# Endpoints de Autenticação
# -------------------------------------------

# Modelo para login
class LoginData(BaseModel):
    nome_usuario: str
    senha: str

@app.post("/register")
def register(nome_usuario: str, senha: str, db: Session = Depends(get_db)):
    hashed_senha = pwd_context.hash(senha)
    novo_usuario = Usuario(nome_usuario=nome_usuario, senha_hash=hashed_senha)
    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)
    logger.info(f"Novo usuário registrado: {nome_usuario}")  # Log de sucesso
    return {"message": "Usuário registrado com sucesso", "user": novo_usuario.nome_usuario}

@app.post("/login")
def login(data: LoginData, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.nome_usuario == data.nome_usuario).first()
    
    if not usuario or not pwd_context.verify(data.senha, usuario.senha_hash):  # Corrigido aqui
        logger.warning(f"Falha na autenticação para o usuário {data.nome_usuario}")  # Log de falha
        raise HTTPException(status_code=401, detail="Credenciais inválidas")

    access_token = criar_acesso_token(data={"sub": usuario.nome_usuario})
    logger.info(f"Usuário {usuario.nome_usuario} autenticado com sucesso")  # Log de sucesso
    return {"access_token": access_token, "token_type": "bearer"}
