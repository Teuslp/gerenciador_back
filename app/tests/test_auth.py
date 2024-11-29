import pytest

def test_register(client):
    response = client.post("/register", json={"nome_usuario": "test_user", "senha": "test_password"})
    assert response.status_code == 200
    assert "Usuário registrado com sucesso" in response.json()["message"]

def test_login(client):
    # Registrar o usuário primeiro
    client.post("/register", json={"nome_usuario": "test_user", "senha": "test_password"})
    
    # Tentar logar com as credenciais
    response = client.post(
        "/login",
        json={"nome_usuario": "test_user", "senha": "test_password"},
    )
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_login_invalid(client):
    # Tentar logar com credenciais inválidas
    response = client.post(
        "/login",
        json={"nome_usuario": "invalid_user", "senha": "invalid_password"},
    )
    assert response.status_code == 401
