from fastapi.testclient import TestClient
from .main import app

client = TestClient(app)


def test_rood():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": {
    "method GET by id": "/pereval/{id} - получить данные о перевале по id",
    "method POST": "/submitData/ - отправить данные о перевале (принимает JSON)",
    "method GET by email": "submitData/{email] - по email получить список отправленных перевалов"
}}