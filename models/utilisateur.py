from db import db

class UtilisateurModel(db.Model):
    __tablename__ = "utilisateurs"

    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(40), nullable=False) 
    prenom = db.Column(db.String(40), nullable=False) 
    numTel = db.Column(db.String(40), nullable=False) 
    email = db.Column(db.String(40), nullable=False) 
    password = db.Column(db.String(40), nullable=False) 
    
    __mapper_args__ = {
            "polymorphic_identity": "utilisateurs",
            "polymorphic_on": "type",
        }
    
    client = db.relationship(
        "ClientModel", back_populates="utilisateurs", lazy=True
    )
