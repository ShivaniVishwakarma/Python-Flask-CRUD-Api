from flask import request
from flask_restx import Resource, fields

from flaskr import db
from flaskr.config.global_error_config import NotFound
from flaskr.config.swagger_config import appNS, appModel
from flaskr.models.application import Application
from flaskr.models.schemas.application_schema import ApplicationSchema


@appNS.route("/")
class ApplicationListView(Resource):
    @appNS.marshal_with(appModel, code=200)
    def get(self):
        applications = Application.query.all()

        return ApplicationSchema(many=True).dump(applications)

    @appNS.expect(appNS.model(
        "Resource",
        {
            "name": fields.String,
            "gitRepo": fields.String,
        }))
    @appNS.marshal_with(appModel, code=201)
    def post(self):
        data = request.get_json()
        application = Application(name=data["name"], gitRepo=data["gitRepo"])

        db.session.add(application)
        db.session.commit()

        return ApplicationSchema().dump(application)


@appNS.route("/<int:id>")
@appNS.response(404, "Application not found")
@appNS.response(200, "Success", appModel)
@appNS.param("id", "Application id")
class ApplicationView(Resource):
    def get(self, id):
        application = find_by_id(id)

        return ApplicationSchema().dump(application)

    def put(self, id):
        application = find_by_id(id)

        data = request.get_json()
        application.name = data["name"]
        application.gitRepo = data["gitRepo"]

        db.session.commit()

        return ApplicationSchema().dump(application)

    @appNS.response(200, "Success", int)
    def delete(self, id):
        application = find_by_id(id)

        db.session.delete(application)
        db.session.commit()

        return id


def find_by_id(id) -> Application:
    entity = Application.query.get(id)
    if entity is None:
        raise NotFound(
            {
                "code": "404",
                "description": "Application not found",
            },
            404,
        )

    return entity
