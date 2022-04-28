from marshmallow import fields

from flaskr import ma
from flaskr.models import environment


class EnvironmentSchema(ma.SQLAlchemyAutoSchema):
    appName = fields.String()

    class Meta:
        model = environment.Environment
        load_instance = True
        include_fk = True

