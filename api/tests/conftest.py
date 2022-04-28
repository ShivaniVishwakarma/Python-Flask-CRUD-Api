import os

import pytest

from flaskr import app, db
from flaskr.models.application import Application
from flaskr.models.deployment import Deployment
from flaskr.models.environment import Environment
from flaskr.models.image import Image


@pytest.fixture
def client():
    app.config["TESTING"] = True
    file_name = 'test.db'

    open(file_name, 'w').close()
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.getcwd() + "\\{}".format(file_name)

    with app.app_context():
        db.create_all()

        application = Application(id = 1, name="app 1", gitRepo="http://")
        db.session.add(application)

        image = Image(id=1, image="test:image:v0", application=application.id)
        db.session.add(image)

        env = Environment(id=1, env="dev", path="test:app 1:v0", application=application.id)
        db.session.add(env)

        env1 = Environment(id=2, env="prod", path="test:app 1:v0", application=application.id)
        db.session.add(env1)

        deployment = Deployment(id=1, application=application.id, status=True, env=env.id, image=image.id)
        db.session.add(deployment)

        db.session.commit()

    with app.test_client() as client:
        yield client
