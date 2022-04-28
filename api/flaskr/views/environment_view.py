from flask import request
from flask_restx import Resource, fields

from flaskr import db
from flaskr.config.swagger_config import envNS, envModel
from flaskr.exceptions.functional_exception import FunctionalException
from flaskr.exceptions.not_found_exception import NotFound
from flaskr.models.application import Application
from flaskr.models.environment import Environment
from flaskr.models.schemas.environment_schema import EnvironmentSchema


@envNS.route("/")
class EnvironmentListView(Resource):
    @envNS.marshal_with(envModel, code=200)
    def get(self):
        environments = Environment.query.all()
        result = []
        for environment in environments:
            application = Application.query.get(environment.application)
            env = {"id": environment.id, "appName": application.name, "env": environment.env, "path": environment.path,
                   "application": environment.application}
            result.append(env)
        return EnvironmentSchema(many=True).dump(result)

    @envNS.expect(envNS.model(
        "Resource",
        {"env": fields.String, "application": fields.String, "path": fields.String},
    ))
    @envNS.marshal_with(envModel, code=201)
    def post(self):
        data = request.get_json()

        environment = Environment(
            env=data["env"], application=data["application"], path=data["path"])

        saved_record = (
            Environment.query.join(Application)
                .filter(
                Application.id == environment.application,
                Environment.env == environment.env,
            )
                .first()
        )

        if saved_record:
            raise FunctionalException({
                "code": "409",
                "description": "Environment-{} already exists for the application-{}".format(
                    environment.env, environment.application
                ),
            },
                409,
            )

        db.session.add(environment)
        application = Application.query.get(data["application"])
        envi = {"id": environment.id, "appName": application.name, "env": data["env"], "path": data["path"],
                "application": data["application"]}
        db.session.commit()
        return EnvironmentSchema().dump(envi)


@envNS.route("/<int:id>")
@envNS.response(404, "Environment not found")
@envNS.response(200, "Success", envModel)
@envNS.param("id", "Environment Id")
class EnvironmentUpdateAndDeleteView(Resource):
    def delete(self, id):
        env = find_by_id(id)

        db.session.delete(env)
        db.session.commit()

        return id

    @envNS.expect(envModel)
    @envNS.marshal_with(envModel, code=201)
    def put(self, id):
        environment = find_by_id(id)

        data = request.get_json()

        environment.env = data["env"]
        environment.path = data["path"]
        environment.application = data["application"]

        db.session.commit()
        application = Application.query.get(data["application"])
        envi = {"id": environment.id, "appName": application.name, "env": data["env"], "path": data["path"],
                "application": data["application"]}

        return EnvironmentSchema().dump(envi)


def find_by_id(id):
    env = Environment.query.get(id)
    if env is None:
        raise NotFound({
            "code": "404",
            "description": "Environment not found",
        },
            404, )

    return env
