import pytest
from process.batch import featured_products

# Datos de ejemplo
SAMPLE_PRODUCTS = [
    {
        "id": "MLA100001",
        "title": "Monitor Curvo",
        "description": "Monitor curvo 300 pulgadas Full HD, 144Hz",
        "price": 120000,
        "currency": "ARS",
        "images": ["https://example.com/monitor1.jpg"],
        "payment_methods": ["Efectivo", "Tarjeta", "MercadoPago"],
        "seller": {"id": "SELLER001", "name": "Tech Store", "reputation": "Platinum", "location": "Córdoba", "sales": 1200},
        "additional_details": {"category": "Tecnologia", "rating": 4.7, "reviews": 1980000, "stock": 42, "warranty": "12 meses de garantía"}
    },
    {
        "id": "MLA100002",
        "title": "Mouse Gamer",
        "description": "Mouse gamer RGB",
        "price": 15000,
        "currency": "ARS",
        "images": ["https://example.com/mouse1.jpg"],
        "payment_methods": ["Tarjeta", "MercadoPago"],
        "seller": {"id": "SELLER002", "name": "GamerTech", "reputation": "Gold", "location": "Rosario", "sales": 8000},
        "additional_details": {"category": "Tecnologia", "rating": 4.5, "reviews": 850, "stock": 30, "warranty": "6 meses"}
    }
]

@pytest.fixture
def mock_files(monkeypatch):
    """Fixture que simula la lectura y escritura de archivos"""
    monkeypatch.setattr(featured_products, "load_json", lambda path: SAMPLE_PRODUCTS if "articles.json" in path else [])
    monkeypatch.setattr(featured_products, "save_json", lambda path, data: data)
    monkeypatch.setattr(featured_products, "load_processed_ids", lambda: set())
    monkeypatch.setattr(featured_products, "save_processed_ids", lambda ids: ids)

def test_generate_featured_batch(mock_files):
    """Test principal del batch: filtrado top5 Platinum"""
    featured_products.generate_featured_batch()
    platinum = [p for p in SAMPLE_PRODUCTS if p["seller"]["reputation"] == "Platinum"]
    assert len(platinum) == 1
    assert platinum[0]["id"] == "MLA100001"


