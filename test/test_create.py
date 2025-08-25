import pytest

# Ejemplo de payload para crear un artículo
NEW_ARTICLE = {
  "title": "PRUEBA DESDE TEST",
  "description": "PRUEBA DESDE TEST",
  "price": 120000,
  "currency": "ARS",
  "images": [
    "https://example.com/monitor1.jpg",
    "https://example.com/monitor2.jpg"
  ],
  "payment_methods": ["Efectivo", "Tarjeta", "MercadoPago"],
  "seller": {
    "name": "Tech Store",
    "rating": 4.8,
    "reputation": "Platinum"
  },
  "additional_details": {
            "stock": 42,
            "rating": 4.7,
            "reviews": 1980000,
            "warranty": "12 meses de garant\u00eda oficial",
            "category": "Tecnologia"
        }
}

def test_create_article_success(client, test_token, monkeypatch):
    from routes import create 
    monkeypatch.setattr(
        create,
        "create_article_process",
        lambda new_data: {
            "success": True,
            "message": "Article created successfully.",
            "article": {"id": "MLA999", **new_data}
        }
    )

    headers = {"Authorization": f"Bearer {test_token}"}
    res = client.post("/create", json=NEW_ARTICLE, headers=headers)

    print(res.get_json())  # para debug
    assert res.status_code == 201
    assert res.json["success"] is True
    assert res.json["message"] == "Article created successfully."
    assert "article" in res.json
    assert res.json["article"]["id"] == "MLA999"



def test_create_article_missing_data(client, test_token):
    # Payload vacío
    headers = {"Authorization": f"Bearer {test_token}"}
    res = client.post("/create", json={}, headers=headers)

    assert res.status_code == 400
    assert res.json["message"] == "No data provided"
    assert res.json["success"] is False


def test_create_article_unauthorized(client):
    res = client.post("/create", json=NEW_ARTICLE)
    assert res.status_code == 401
    assert "error" in res.json
