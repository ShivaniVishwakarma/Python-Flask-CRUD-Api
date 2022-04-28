from datetime import datetime
from flaskr import db


class Image(db.Model):
    __tablename__ = "images"

    id = db.Column(db.Integer, primary_key=True)
    application = db.Column(db.Integer(), db.ForeignKey('applications.id'))
    image = db.Column(db.String(50), nullable=False)
    createdDate = db.Column("created_date", db.DateTime(), default=datetime.now())

    def __repr__(self) -> str:
        return "{} > {}".format(self.application, self.image)
