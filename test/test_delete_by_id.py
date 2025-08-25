#En la base cree un usuario testPruebas,testPruebas
#Prueba de que 1 necesito un token y 2 que devuelva un dict
def test_delete_article_success(client, test_token, monkeypatch):
    from routes import delete_by_id
    monkeypatch.setattr(
        delete_by_id,
        "delete_article_process",
        lambda article_id: {"success": True, "message": "Article deleted successfully."}
    )
    headers = {"Authorization": f"Bearer {test_token}"}
    res = client.delete("/delete_by_id/MLA100015", headers=headers)
    assert res.status_code == 200
    assert res.json == {
        "message": "Article deleted successfully.",
        "success": True
    }

def test_delete_article_not_found(client, test_token, monkeypatch):
    from routes import delete_by_id
    monkeypatch.setattr(
        delete_by_id,
        "delete_article_process",
        lambda article_id: {"success": False, "message": "Article not found"}
    )

    headers = {"Authorization": f"Bearer {test_token}"}
    res = client.delete("/delete_by_id/MLA999999", headers=headers)

    assert res.status_code == 404
    assert res.json == {
        "message": "Article not found",
        "success": False
    }
