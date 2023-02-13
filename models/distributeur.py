from db import db
from models.utilisateur import UtilisateurModel

class DistributeurModel(UtilisateurModel):
    __tablename__ = 'distributeurs'

    id = db.Column(db.Integer, db.ForeignKey("utilisateurs.id"), primary_key=True)
    
    __mapper_args__ = {
        "polymorphic_identity": "distributeurs"
    }
    
    code_Agent = db.Column(db.String(40), nullable=False)
    plaque = db.Column(db.String(80), nullable=False)
    
    livraison = db.relationship(
        "LivraisonModel", back_populates="distributeurs", lazy=True
    )
    
   