from unittest import TestCase

from flask import json


def test_get_image(client):
    response = client.get("/images/")
    data = response.get_json()

    assert response.status_code == 200
    assert len(data) == 1


def test_create_image(client):
    response = client.post("/images/", data=json.dumps({"image": "test:image:v1", "application": "1"}),
                           content_type='application/json', )

    data = response.get_json()

    assert response.status_code == 200
    assert response.data is not None
    assert data["image"] == "test:image:v1"
    assert data["application"] == "1"


def test_delete_image_by_id(client):
    response = client.delete("/images/1")

    assert response.status_code == 200
    assert response.data == b'1\n'


# Error cases

def test_throw_error_when_image_name_and_application_is_duplicate(client):
    response = client.post("/images/", data=json.dumps({"image": "test:image:v0", "application": "1"}),
                           content_type='application/json', )

    data = response.get_json()

    assert response.status_code == 409
    assert data["code"] == "409"
    assert data["description"] == "Image - test:image:v0 already exists for the application- 1"


def test_throw_error_when_delete_with_invalid_id(client):
    response = client.delete("/images/10")

    data = response.get_json()

    assert response.status_code == 404

    TestCase().assertDictEqual(data, {"code": "404", "description": "Image not found"})
