import pytest
from fastapi import HTTPException
from app.models.livro import Livro

def test_criar_livro(client, db, create_user):
    # Criar livro
    response = client.post(
        "/livros/",
        json={"titulo": "Livro Teste", "autor": "Autor Teste", "ano": 2024, "genero": "Ficção"},
        headers={"Authorization": "Bearer dummy_token"},  # Substitua com um token válido
    )
    assert response.status_code == 201
    assert "titulo" in response.json()
    assert response.json()["titulo"] == "Livro Teste"

def test_listar_livros(client, db, create_user):
    # Listar livros
    response = client.get("/livros/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_buscar_livro(client, db, create_user):
    # Criar um livro no banco de dados
    novo_livro = Livro(titulo="Livro de Teste", autor="Autor Teste", ano=2024, genero="Ficção")
    db.add(novo_livro)
    db.commit()
    db.refresh(novo_livro)

    # Buscar livro pelo ID
    response = client.get(f"/livros/{novo_livro.id}")
    assert response.status_code == 200
    assert response.json()["titulo"] == "Livro de Teste"

def test_atualizar_livro(client, db, create_user):
    # Criar livro
    novo_livro = Livro(titulo="Livro para Atualizar", autor="Autor Teste", ano=2024, genero="Ficção")
    db.add(novo_livro)
    db.commit()
    db.refresh(novo_livro)

    # Atualizar livro
    response = client.put(
        f"/livros/{novo_livro.id}",
        json={"titulo": "Livro Atualizado", "autor": "Autor Teste", "ano": 2024, "genero": "Aventura"},
        headers={"Authorization": "Bearer dummy_token"},  # Substitua com um token válido
    )
    assert response.status_code == 200
    assert response.json()["titulo"] == "Livro Atualizado"

def test_deletar_livro(client, db, create_user):
    # Criar livro
    novo_livro = Livro(titulo="Livro para Deletar", autor="Autor Teste", ano=2024, genero="Ficção")
    db.add(novo_livro)
    db.commit()
    db.refresh(novo_livro)

    # Deletar livro
    response = client.delete(f"/livros/{novo_livro.id}", headers={"Authorization": "Bearer dummy_token"})
    assert response.status_code == 200
    assert response.json() == {"message": "Livro deletado com sucesso"}
