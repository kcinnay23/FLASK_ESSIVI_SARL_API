from db import db

class ClientModel(db.Model):
    __tablename__ = "clients"

    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(40), unique=True, nullable=False)
    prenom = db.Column(db.String(40), unique=True, nullable=False)
    numTel = db.Column(db.String(40), unique=True, nullable=False)
    adresse = db.Column(db.String(40), unique=True, nullable=False)
    
    utilisateur_id = db.Column(
        db.Integer, db.ForeignKey("utilisateurs.id"), unique=False, nullable=False
    )
    
    depot = db.relationship(
        "DepotModel", back_populates="clients", lazy=True 
    )
