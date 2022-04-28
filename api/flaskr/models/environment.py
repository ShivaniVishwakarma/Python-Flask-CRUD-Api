from datetime import datetime

from flaskr import db


class Environment(db.Model):
    __tablename__ = "environments"

    id = db.Column(db.Integer, primary_key=True)
    env = db.Column(db.String(50), nullable=False)
    application = db.Column(db.Integer(), db.ForeignKey('applications.id'))
    path = db.Column(db.String(100), nullable=False)

    def __repr__(self) -> str:
        return "{} : {}".format(
            self.env, self.application
        )
