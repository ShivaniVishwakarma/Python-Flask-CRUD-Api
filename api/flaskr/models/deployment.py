from datetime import datetime

from flaskr import db


class Deployment(db.Model):
    __tablename__ = "deployments"

    id = db.Column(db.Integer, primary_key=True)
    application = db.Column(db.Integer(), db.ForeignKey('applications.id'))
    env = db.Column(db.Integer(), db.ForeignKey('environments.id'))
    image = db.Column(db.Integer(), db.ForeignKey('images.id'))
    status = db.Column(db.Boolean, default=False)
    createdDate = db.Column("created_date", db.DateTime(), default=datetime.now())
