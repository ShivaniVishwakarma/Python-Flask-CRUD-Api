from datetime import datetime
from flaskr import db

class Application(db.Model):
    __tablename__ = "applications"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    gitRepo = db.Column("git_repo", db.String(100), nullable=False)
    createdDate = db.Column("created_date", db.DateTime(), default=datetime.now())

    def __repr__(self) -> str:
        return "{} > {}".format(self.name, self.gitRepo)
