from flaskr import api
from flask_restx import fields

# Application Model definition
appNS = api.namespace("applications", description="Application operations")
appCreateResourceFields = appNS.model(
    "Resource",
    {
        "name": fields.String,
        "gitRepo": fields.String,
    },
)
appModel = api.model(
    "Model",
    {
        "id": fields.Integer,
        "name": fields.String,
        "gitRepo": fields.String,
        "createdDate": fields.DateTime,
    },
)


# Environment Model definition
envNS = api.namespace("environments", description="Environment operations")
envCreateResourceFields = envNS.model(
    "Resource",
    {"env": fields.String, "application": fields.String, "path": fields.String},
)
envModel = api.model(
    "Model",
    {
        "id": fields.Integer,
        "env": fields.String,
        "application": fields.Integer,
        "appName": fields.String,
        "path": fields.String,
    },
)

# Image Model definition
imageNS = api.namespace("images", description="Image operations")
imageCreationModel = api.model(
    "Resource",
    {"image": fields.String, "application": fields.String, "path": fields.String},
)
imgModel = imageNS.model(
    "Model",
    {
        "id": fields.Integer,
        "image": fields.String,
        "application": fields.String,
        "appName": fields.String,
        "createdDate": fields.DateTime,
    },
)

# Deployment Model Definition
deployNS = api.namespace("deployments", description="Deployment operations")
deployCreationModel = deployNS.model(
    "Resource",
    {"application": fields.String, "image": fields.String}
)
deployModel = api.model(
    "Model",
    {
        "id": fields.Integer,
        "application": fields.String,
        "env": fields.String,
        "image": fields.String,
        "status": fields.Boolean,
        "createdDate": fields.DateTime
    },
)
