from flask import request
from flask_restx import Resource, fields

from flaskr import db
from flaskr.config.swagger_config import deployNS, deployModel
from flaskr.exceptions.functional_exception import FunctionalException
from flaskr.exceptions.not_found_exception import NotFound
from flaskr.models.application import Application
from flaskr.models.deployment import Deployment
from flaskr.models.environment import Environment
from flaskr.models.image import Image
from flaskr.models.schemas.deployment_schema import DeploymentSchema
from flaskr.models.schemas.image_schema import ImageSchema
from flaskr.views.application_view import ApplicationView


@deployNS.route("/")
class DeploymentsListView(Resource):
    @deployNS.marshal_with(deployModel, code=200)
    def get(self):
        deployments = Deployment.query.all()
        result = []
        for deployment in deployments:
            application = Application.query.get(deployment.application)
            environment = Environment.query.get(deployment.env)
            image = Image.query.get(deployment.image)
            dep = {"id": deployment.id, "application": application.name, "env": environment.env, "image": image.image,
                   "status": deployment.status, "createdDate": deployment.createdDate}
            result.append(dep)
        return DeploymentSchema(many=True).dump(result)


@deployNS.route("/<int:id>")
@deployNS.response(404, "Deployment not found")
@deployNS.response(200, "Success", deployModel)
@deployNS.param("id", "Deployment id")
class DeploymentView(Resource):

    def get(self, id):
        deployment = findById(id)
        application = Application.query.get(deployment.application)
        environment = Environment.query.get(deployment.env)
        image = Image.query.get(deployment.image)
        dep = {"id": deployment.id, "application": application.name, "env": environment.env, "image": image.image,
               "status": deployment.status, "createdDate": deployment.createdDate}
        return DeploymentSchema().dump(dep)

    @deployNS.response(200, "Success", int)
    def delete(self, id):
        deployment = findById(id)
        db.session.delete(deployment)
        db.session.commit()
        return id


@deployNS.route("/createVersion")
class DeploymentsCreateVersionView(Resource):

    @deployNS.expect(deployNS.model(
        "Resource",
        {"application": fields.String, "image": fields.String}
    ))
    @deployNS.marshal_with(deployModel, code=201)
    def post(self):
        data = request.get_json()
        appl = find_app_by_name(data["application"])
        image = Image(image=data["image"], application=appl.id)

        image_record = (
            Image.query.join(Application)
                .filter(
                Application.name == data["application"], Image.image == image.image
            )
                .first()
        )

        if image_record:
            raise FunctionalException(
                {
                    "code": "409",
                    "description": "Image - {} already exists for the application- {}".format(
                        image.image, image.application
                    ),
                },
                409,
            )

        db.session.add(image)
        db.session.commit()
        db.session.refresh(image)

        return ImageSchema().dump(image)


@deployNS.route("/deployVersion")
@deployNS.response(404, "Deployment not found")
@deployNS.response(200, "Success", deployModel)
class DeploymentsDeployVersionView(Resource):

    @deployNS.expect(deployModel)
    @deployNS.marshal_with(deployModel, code=201)
    def put(self):
        data = request.get_json()
        application = data["application"]
        image = data["image"]
        envs = data["env"]

        app = findAppById(application)
        img = findImgById(image)

        result = []

        for env in envs:
            envi = findEnvById(env)
            deployment_record = db.session.query(Deployment) \
                .filter(
                Deployment.application == application,
                Deployment.image == image,
                Deployment.env == env
            ).all()

            if deployment_record:
                raise FunctionalException(
                    {
                        "code": "409",
                        "description": "Deployment already exists for the application- {} , Image- {} and Environment- {}".format(
                            app.name, img.image, envi.env
                        ),
                    },
                    409,
                )

            deployment = Deployment(application=application, image=image, env=env, status=True)
            result.append(deployment)
            db.session.add(deployment)
        db.session.commit()

        return DeploymentSchema(many=True).dump(result)


def findById(id) -> Deployment:
    entity = Deployment.query.get(id)
    if entity is None:
        raise NotFound(
            {
                "code": "404",
                "description": "Deployment not found",
            },
            404,
        )

    return entity


def findAppById(id) -> Application:
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


def findImgById(id) -> Image:
    entity = Image.query.get(id)
    if entity is None:
        raise NotFound(
            {
                "code": "404",
                "description": "Image not found",
            },
            404,
        )

    return entity


def findEnvById(id) -> Environment:
    entity = Environment.query.get(id)
    if entity is None:
        raise NotFound(
            {
                "code": "404",
                "description": "Environment not found",
            },
            404,
        )

    return entity


def find_app_by_name(appName) -> Application:
    entity = Application.query.filter_by(name=appName).first()
    if entity is None:
        raise NotFound(
            {
                "code": "404",
                "description": "Application not found",
            },
            404,
        )

    return entity