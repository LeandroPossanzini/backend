import json
import pytest
from system import articles_repository as repo

@pytest.fixture
def temp_articles_file(tmp_path, monkeypatch):
    # archivo temporal que reemplaza a ARTICLES_FILE
    file = tmp_path / "articles.json"
    file.write_text(json.dumps([
        {"id": "MLA100001", "title": "Monitor Samsung"},
        {"id": "MLA100002", "title": "Teclado Mecánico"},
        {"id": "MLA100003", "title": "Mouse Logitech"}
    ]), encoding="utf-8")
    monkeypatch.setattr(repo, "ARTICLES_FILE", str(file))
    return file

def test_get_first_matching_articles_found(temp_articles_file):
    results = repo.get_first_matching_articles("monitor")
    assert len(results) == 1
    assert results[0]["id"] == "MLA100001"

def test_get_first_matching_articles_not_found_returns_first(temp_articles_file):
    results = repo.get_first_matching_articles("inexistente", max_results=2)
    # como no hay coincidencias, trae los primeros 2
    assert len(results) == 2
    assert results[0]["id"] == "MLA100001"

def test_update_article_system_success(temp_articles_file):
    updated = repo.update_article_system("MLA100002", {"title": "Teclado Redragon"})
    assert updated is True
    data = json.loads(temp_articles_file.read_text(encoding="utf-8"))
    assert any(a["title"] == "Teclado Redragon" for a in data)

def test_update_article_system_not_found(temp_articles_file):
    updated = repo.update_article_system("MLA999999", {"title": "Nada"})
    assert updated is False

def test_delete_article_system_success(temp_articles_file):
    deleted = repo.delete_article_system("MLA100003")
    assert deleted is True
    data = json.loads(temp_articles_file.read_text(encoding="utf-8"))
    ids = [a["id"] for a in data]
    assert "MLA100003" not in ids

def test_delete_article_system_not_found(temp_articles_file):
    deleted = repo.delete_article_system("MLA999999")
    assert deleted is False

def test_create_article_system_success(temp_articles_file):
    new_data = {"title": "Nuevo producto"}
    article = repo.create_article_system(new_data)
    assert article["id"].startswith("MLA")
    assert article["title"] == "Nuevo producto"
    data = json.loads(temp_articles_file.read_text(encoding="utf-8"))
    assert any(a["id"] == article["id"] for a in data)
