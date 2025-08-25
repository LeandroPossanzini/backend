import json
import pytest
from system import featured_repository as repo

@pytest.fixture
def temp_featured_file(tmp_path, monkeypatch):
    # archivo temporal con productos destacados
    file = tmp_path / "featured_products.json"
    file.write_text(json.dumps([
        {"id": "MLA200001", "title": "Producto Destacado 1"},
        {"id": "MLA200002", "title": "Producto Destacado 2"},
        {"id": "MLA200003", "title": "Producto Destacado 3"}
    ]), encoding="utf-8")
    monkeypatch.setattr(repo, "FEATURED_FILE", str(file))
    return file

def test_get_all_featured_success(temp_featured_file):
    featured = repo.get_all_featured()
    assert len(featured) == 3
    assert featured[0]["id"] == "MLA200001"

def test_get_all_featured_file_not_found(tmp_path, monkeypatch):
    fake_file = tmp_path / "no_existe.json"
    monkeypatch.setattr(repo, "FEATURED_FILE", str(fake_file))
    result = repo.get_all_featured()
    assert result == []  # debe devolver lista vacía

def test_update_featured_success(temp_featured_file):
    updated = repo.update_featured("MLA200002", {"title": "Producto Actualizado"})
    assert updated is True
    data = json.loads(temp_featured_file.read_text(encoding="utf-8"))
    assert any(p["title"] == "Producto Actualizado" for p in data)

def test_update_featured_not_found(temp_featured_file):
    updated = repo.update_featured("MLA999999", {"title": "No Existe"})
    assert updated is False

def test_delete_featured_system_success(temp_featured_file):
    deleted = repo.delete_featured_system("MLA200003")
    assert deleted is True
    data = json.loads(temp_featured_file.read_text(encoding="utf-8"))
    ids = [p["id"] for p in data]
    assert "MLA200003" not in ids

def test_delete_featured_system_not_found(temp_featured_file):
    deleted = repo.delete_featured_system("MLA999999")
    assert deleted is False
