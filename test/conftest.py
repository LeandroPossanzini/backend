import sys
import jwt
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from process.auth_service import SECRET_KEY

import pytest
from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

#Cree este usuario para poder hacer pruebas testPruebas,testPruebas
@pytest.fixture
def test_token():
    payload = {"username": "testPruebas"}
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token if isinstance(token, str) else token.decode("utf-8")