from unittest import TestCase

from flask import json


def test_get_environments(client):
    response = client.get("/environments/")
    data = response.get_json()

    assert response.status_code == 200
    assert len(data) == 2
    assert data[0]['application'] == 1
    assert data[0]['env'] == "dev"
    assert data[0]['path'] == "test:app 1:v0"


def test_create_environment(client):
    response = client.post("/environments/",
                           data=json.dumps({"env": "stage", "path": "stage:app 1:v1", "application": "1"}),
                           content_type='application/json', )

    data = response.get_json()

    assert response.status_code == 200
    assert response.data is not None
    assert data["env"] == "stage"
    assert data["application"] == 1
    assert data["path"] == "stage:app 1:v1"

    response = client.get("/environments/")
    data = response.get_json()
    assert len(data) == 3


def test_delete_application_by_id(client):
    response = client.delete("/environments/1")

    assert response.status_code == 200
    assert response.data == b'1\n'

    response = client.get("/environments/")
    assert response.status_code == 200
    assert len(response.get_json()) == 1


# Error cases


def test_error_when_env_already_exists_for_application(client):
    response = client.post("/environments/",
                           data=json.dumps({"env": "dev", "path": "stage:app 1:v1", "application": "1"}),
                           content_type='application/json', )

    data = response.get_json()

    assert response.status_code == 409
    assert response.data is not None
    assert data["code"] == "409"
    assert data["description"] == "Environment-dev already exists for the application-1"


def test_throw_error_delete_with_invalid_id(client):
    response = client.delete("/environments/10")

    data = response.get_json()

    assert response.status_code == 404

    TestCase().assertDictEqual(data, {"code": "404", "description": "Environment not found"})
