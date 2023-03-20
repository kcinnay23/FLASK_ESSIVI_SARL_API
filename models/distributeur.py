from db import db
from models.utilisateur import UtilisateurModel


class DistributeurModel(UtilisateurModel):
    __tablename__ = 'distributeurs'

    id = db.Column(db.Integer, db.ForeignKey("utilisateurs.id"), primary_key=True)

    __mapper_args__ = {
        "polymorphic_identity": "distributeur"
    }

    code_agent = db.Column(db.String(40), nullable=False)
    plaque_voiture = db.Column(db.String(80), nullable=False)

    livraisons = db.relationship(
        "LivraisonModel", back_populates="distributeurs", lazy=True
    )
