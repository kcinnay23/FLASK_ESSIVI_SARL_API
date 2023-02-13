from db import db

class DepotModel(db.Model):
    __tablename__ = "depots"

    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(40), unique=True, nullable=False)
    long = db.Column(db.Float, unique=True, nullable=False)
    lat = db.Column(db.Float, unique=True, nullable=False)

    client_id = db.Column(
        db.Integer, db.ForeignKey("clients.id"), unique=False, nullable=False
    )



