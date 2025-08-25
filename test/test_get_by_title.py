def test_get_by_title_success(client, monkeypatch):
    res = client.get("/get_by_title?title=disco&username=testPruebas")

    assert res.status_code == 200
    assert isinstance(res.json, list)

def test_get_by_title_missing_title(client):

    res = client.get("/get_by_title")
    assert res.status_code == 400
    assert "error" in res.json


