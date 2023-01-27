from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
    "GET by id": "/pereval/{id} - данные о перевале по id",
    "POST": "/submitData/ - отправить данные о перевале (принимает JSON)",
    "GET by email": "submitData/email/{email] - по email получить список отправленных перевалов",
    "PATCH": "submitData/{id} - отредактировать запись о перевале, принимает JSON"
    }


def test_read_pereval():
    response = client.get("/pereval/1/")
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "add_time": "2021-09-22T13:18:13",
        "beauty_title": "пер.",
        "title": "Пхия",
        "other_titles": "Триев",
        "connect": None,
        "user": {
            "email": "user@email.ltd",
            "phone": 79031234567,
            "fam": "Пупкин",
            "name": "Василий",
            "otc": "Иванович"
        },
        "coords": {
            "latitude": "45.3842",
            "longitude": "7.1525",
            "height": "1200"
        },
        "level": {
            "winter": "",
            "summer": "1A",
            "autumn": "1A",
            "spring": ""
        },
        "status": "pending"
    }


def test_read_pereval_if_not_exists():
    response = client.get("/pereval/1001/")
    assert response.status_code == 400
    assert response.json() == {
        "status": 400,
        "message": "Перевал не найден",
        "id": "1001"
    }


def test_get_perevel_list_by_user_email():
    response = client.get("/submitData/email/user@email.ltd")
    assert response.status_code == 200
    assert response.json() == {
        "pereval": [
            {
             "id": 1,
             "title": "Пхия",
             "other_titles": "Триев",
             "add_time": "2021-09-22T13:18:13",
             "status": "pending"
            }
        ]
    }


def test_get_perevel_list_by_user_email_not_exists():
    response = client.get("/submitData/email/sampleuser@sampleemail.com")
    assert response.status_code == 400
    assert response.json() == {
        "status": 400,
        "message": "Пользователь с данным email не зарегистрирован"
    }
