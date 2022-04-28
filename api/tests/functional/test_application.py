from unittest import TestCase

from flask import json


def test_get_application(client):
    # mimetype = 'application/json'
    # headers = {
    #    'Content-Type': mimetype,
    #    'Accept': mimetype
    # }
    # response = client.post("/applications/", data=json.dumps({"name": "saleem", "gitRepo": "http:"}),
    #                      content_type='application/json', )

    response = client.get("/applications/")
    data = response.get_json()

    assert response.status_code == 200
    assert len(data) == 1


def test_create_application(client):
    response = client.post("/applications/", data=json.dumps({"name": "app 2", "gitRepo": "http://test.com"}),
                           content_type='application/json', )

    data = response.get_json()

    assert response.status_code == 200
    assert response.data is not None
    assert data["name"] == "app 2"
    assert data["gitRepo"] == "http://test.com"


def test_get_by_id(client):
    response = client.get("/applications/1")

    data = response.get_json()

    assert response.status_code == 200
    assert data["name"] == "app 1"
    assert data["gitRepo"] == "http://"


def test_delete_application_by_id(client):
    response = client.delete("/applications/1")

    assert response.status_code == 200
    assert response.data == b'1\n'

    getByIdResponse = client.get("/applications/1")
    assert getByIdResponse.status_code == 404


# Error cases

def test_throw_error_when_get_by_id_not_found(client):
    response = client.get("/applications/10")

    data = response.get_json()

    assert response.status_code == 404

    TestCase().assertDictEqual(data, {"code": "404", "description": "Application not found"})


def test_throw_error_delete_with_invalid_id(client):
    response = client.delete("/applications/10")

    data = response.get_json()

    assert response.status_code == 404

    TestCase().assertDictEqual(data, {"code": "404", "description": "Application not found"})
