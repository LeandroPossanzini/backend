VALID_USER = {"username": "testPruebas", "password": "testPruebas"}
INVALID_USER = {"username": "userfake", "password": "wrongpass"}

def test_login_success(client, monkeypatch):
    
    res = client.post("/login", json=VALID_USER)

    assert res.status_code == 200
    assert res.json["message"] == "Login successful"
    assert "token" in res.json
    assert res.json["user"] == VALID_USER["username"]


def test_login_invalid_credentials(client, monkeypatch):

    res = client.post("/login", json=INVALID_USER)
    # print(res.get_json())
    assert res.status_code == 401
    assert res.json["error"] == "Invalid username or password"


def test_login_missing_data(client):

    res = client.post("/login", json={"username": "", "password": ""})

    assert res.status_code == 400
    assert res.json["error"] == "Username y password son requeridos"
