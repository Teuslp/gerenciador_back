import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal, engine, Base
from app.models.livro import Livro
from app.models.categoria import Categoria
from app.models.user import Usuario

# Fixture para criar um banco de dados de teste
@pytest.fixture(scope="module")
def db():
    # Cria o banco de dados em memória para os testes
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    yield db
    db.close()
    Base.metadata.drop_all(bind=engine)

# Fixture para o cliente HTTP
@pytest.fixture()
def client():
    client = TestClient(app)
    return client

# Fixture para criar um usuário de teste
@pytest.fixture()
def create_user(db):
    usuario = Usuario(nome_usuario="test_user", senha_hash="test_password")
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return usuario
