from marshmallow import fields

from flaskr import ma

from flaskr.models.deployment import Deployment


class DeploymentSchema(ma.SQLAlchemyAutoSchema):

    application = fields.String()
    env = fields.String()
    image = fields.String()

    class Meta:
        model = Deployment
        load_instance = True
        include_fk = True

