from flask import request
from flask_restx import Resource, fields

from flaskr import db
from flaskr.config.swagger_config import imageNS, imgModel
from flaskr.exceptions.functional_exception import FunctionalException
from flaskr.exceptions.not_found_exception import NotFound
from flaskr.models.application import Application
from flaskr.models.image import Image
from flaskr.models.schemas.image_schema import ImageSchema


@imageNS.route("/")
class ImageListView(Resource):
    @imageNS.marshal_with(imgModel, code=200)
    def get(self):
        images = Image.query.all()
        result = []
        for image in images:
            application = Application.query.get(image.application)
            img = {"id": image.id, "appName": application.name, "image": image.image, "createdDate": image.createdDate,
                   "application": image.application}
            result.append(img)
        return ImageSchema(many=True).dump(result)

    @imageNS.expect(imageNS.model(
        "Model",
        {
            "id": fields.Integer,
            "image": fields.String,
            "application": fields.String,
            "createdDate": fields.DateTime,
        },
    ))
    @imageNS.marshal_with(imgModel, code=201)
    def post(self):
        data = request.get_json()
        image = Image(image=data["image"])

        saved_record = (
            Image.query.join(Application)
                .filter(
                Application.id == data["application"], Image.image == image.image
            )
                .first()
        )

        if saved_record:
            raise FunctionalException(
                {
                    "code": "409",
                    "description": "Image - {} already exists for the application- {}".format(
                        image.image, data["application"]
                    ),
                },
                409,
            )

        image.application = data["application"]

        db.session.add(image)
        db.session.commit()

        return ImageSchema().dump(image)


@imageNS.route("/<int:id>")
@imageNS.param("id", "Image Id")
@imageNS.response(404, "Image not found")
@imageNS.response(200, "Success", imgModel)
class ImageDeleteAndUpdateView(Resource):
    def delete(self, id):
        img = find_by_id(id)

        db.session.delete(img)
        db.session.commit()

        return id

    @imageNS.expect(imgModel)
    @imageNS.marshal_with(imgModel, code=201)
    def put(self, id):
        image = find_by_id(id)

        data = request.get_json()

        image.image = data["image"]
        image.application = data["application"]

        db.session.commit()

        return ImageSchema().dump(image)


def find_by_id(id):
    image = Image.query.get(id)

    if image is None:
        raise NotFound({
            "code": "404",
            "description": "Image not found",
        },
            404, )

    return image
