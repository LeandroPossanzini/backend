#Testeo que un usuario no se pueda volver a registrar
def test_register_user(client):
    payload = {
        "username": "leandro",
        "password": "leandro2"
    }
    res = client.post("/register", json=payload)
    assert res.status_code == 409

#Testeo que no se pueda registrar sin usuario
def test_register_missing_username(client):
    payload = {"password": "Password123"}
    res = client.post("/register", json=payload)
    assert res.status_code == 400

#Testeo que no se pueda registrar sin pasword
def test_register_missing_password(client):
    payload = {"username": "usuario_test"}
    res = client.post("/register", json=payload)
    assert res.status_code == 400

#Testeo qeu no se pueda registar sin body
def test_register_empty_body(client):
    res = client.post("/register", json={})
    assert res.status_code == 400

    data = res.get_json()
    assert "error" in data
