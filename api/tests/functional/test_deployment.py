from unittest import TestCase

from flask import json


def test_get_deployment(client):
    response = client.get("/deployments/")
    data = response.get_json()

    assert response.status_code == 200
    assert len(data) == 1


def test_get_deployment_by_id(client):
    response = client.get("/deployments/1")
    data = response.get_json()
    assert response.status_code == 200
    assert data["application"] == "app 1"
    assert data["image"] == "test:image:v0"
    assert data["env"] == "dev"


def test_delete_deployment_by_id(client):
    response = client.delete("/deployments/1")

    assert response.status_code == 200
    assert response.data == b'1\n'

    getByIdResponse = client.get("/deployments/1")
    assert getByIdResponse.status_code == 404


def test_create_version(client):
    response = client.post("deployments/createVersion",  data=json.dumps({"application": "app 1", "image": "test:image:v1"}),
                           content_type='application/json')

    data = response.get_json()

    assert response.status_code == 200
    assert response.data is not None
    assert data["application"] == "1"
    assert data["image"] == "test:image:v1"


def test_deploy_version_when_deployment_already_exist(client):
    response = client.put("deployments/deployVersion",  data=json.dumps({"application": "1", "image": 1, "env": [1]}),
                           content_type='application/json')

    data = response.get_json()

    assert response.status_code == 409
    assert response.data is not None
    assert data["description"] == "Deployment already exists for the application- app 1 , Image- test:image:v0 and Environment- dev"


def test_deploy_version(client):
    response = client.put("deployments/deployVersion",  data=json.dumps({"application": "1", "image": 1, "env": [1]}),
                           content_type='application/json')

    data = response.get_json()

    assert response.status_code == 200
    assert response.data is not None



def test_throw_error_when_get_deployment_by_id_not_found(client):
    response = client.get("/deployments/10")
    data = response.get_json()
    assert response.status_code == 404
    TestCase().assertDictEqual(data, {"code": "404", "description": "Deployment not found"})


def test_throw_error_delete_deployment_with_invalid_id(client):
    response = client.delete("/deployments/10")
    data = response.get_json()
    assert response.status_code == 404
    TestCase().assertDictEqual(data, {"code": "404", "description": "Deployment not found"})
