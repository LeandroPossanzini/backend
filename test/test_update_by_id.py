import pytest

# Datos de ejemplo para actualizar un artículo
ARTICLE_PAYLOAD = {
    "title": "Prueba desde TEST",
    "description": "Prueba desde TEST",
    "price": 15999.99,
    "currency": "ARS",
    "images": ["https://example.com/image1.jpg"],
    "payment_methods": ["MercadoPago", "Tarjeta"],
    "seller": {
        "id": "seller123",
        "name": "Vendedor Ejemplo",
        "location": "Córdoba",
        "reputation": "Excelente",
        "sales": 100
    },
    "additional_details": {
        "category": "Electrónica",
        "rating": 5,
        "reviews": 10,
        "stock": 20,
        "warranty": "12 meses"
    }
}

#Simulo la respuesta del backend 
#Se prueba que funcione con el token 
def test_update_article_success(client, test_token, monkeypatch):
    from routes import update_by_id
    monkeypatch.setattr(
        update_by_id,
        "update_article_process",
        lambda article_id, data: {"success": True, "message": "Article updated successfully."}
    )

    headers = {"Authorization": f"Bearer {test_token}"}
    res = client.put("/update_by_id/MLA100015", headers=headers, json=ARTICLE_PAYLOAD)

    assert res.status_code == 200
    assert res.json == {
        "message": "Article updated successfully.",
        "success": True
    }

#Si no encuentra el articulo
def test_update_article_not_found(client, test_token, monkeypatch):
    from routes import update_by_id
    monkeypatch.setattr(
        update_by_id,
        "update_article_process",
        lambda article_id, data: {"success": False, "message": "Article not found"}
    )

    headers = {"Authorization": f"Bearer {test_token}"}
    res = client.put("/update_by_id/MLA00015", headers=headers, json=ARTICLE_PAYLOAD)

    assert res.status_code == 404
    assert res.json == {
        "message": "Article not found",
        "success": False
    }

#Si no tengo datos 
def test_update_article_no_data(client, test_token, monkeypatch):
    from routes import update_by_id
    monkeypatch.setattr(
        update_by_id,
        "update_article_process",
        lambda article_id, data: {"success": False, "message": "No data provided"} if not data else {"success": True, "message": "Article updated successfully."}
    )

    headers = {"Authorization": f"Bearer {test_token}"}
    res = client.put("/update_by_id/MLA100015", headers=headers, json={})

    assert res.status_code == 400
    assert res.json == {
        "message": "No data provided",
        "success": False
    }
