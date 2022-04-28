from marshmallow import fields

from flaskr import ma
from flaskr.models import image


class ImageSchema(ma.SQLAlchemyAutoSchema):
    appName = fields.String()

    class Meta:
        model = image.Image
        load_instance = True
        include_fk = True
