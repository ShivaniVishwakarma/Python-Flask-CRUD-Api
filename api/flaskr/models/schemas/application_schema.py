from flaskr import ma
from flaskr.models.application import Application
from marshmallow import fields


class ApplicationSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Application
        load_instance = True

