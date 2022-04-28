import os

from flask import Flask
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate, upgrade
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import database_exists, create_database

api = Api(doc="/")
db = SQLAlchemy()
migrate = Migrate()
ma = Marshmallow()


def create_app_database(db_url):
    if not database_exists(db_url):
        create_database(db_url)
        print("created database...")


def create_app():
    app = Flask(__name__)
    CORS(app)

    # Initialize database
    user = os.getenv("POSTGRES_USER")
    password = os.getenv("POSTGRES_PASSWORD")
    database = os.getenv("POSTGRES_DB")
    host = os.getenv("POSTGRES_HOST")

    print("connection details : ",user, password, database, host)

    # Initialize database
    app.config[
        "SQLALCHEMY_DATABASE_URI"
    ] = f"postgresql://{user}:{password}@{host}:5432/{database}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    create_app_database(app.config["SQLALCHEMY_DATABASE_URI"])
    db.init_app(app)

    from flaskr.models.application import Application
    from flaskr.models.environment import Environment
    from flaskr.models.image import Image
    from flaskr.models.deployment import Deployment

    # Initialize swagger
    api.init_app(app)
    # Initialize migration
    migrate.init_app(app, db)
    # Initialize object serialization / deserialization
    ma.init_app(app)

    app.config["SQLALCHEMY_ECHO"] = 1

    return app


app = create_app()

with app.app_context():
    upgrade()


from flaskr.views import application_view, environment_view, image_view, deployment_view
from flaskr.config import auth0_config, global_error_config
