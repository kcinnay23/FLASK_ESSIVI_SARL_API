from db import db
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

class UtilisateurModel(db.Model):
    __tablename__ = "utilisateurs"
    
    """id: Mapped[int] = mapped_column(primary_key=True)
    nom: Mapped[str]
    prenom: Mapped[str]
    numTel: Mapped[str]
    email: Mapped[str]
    password: Mapped[str]"""

    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(40), nullable=False) 
    prenom = db.Column(db.String(40), nullable=False) 
    numTel = db.Column(db.String(40), nullable=False) 
    email = db.Column(db.String(40), nullable=False) 
    password = db.Column(db.String(40), nullable=False)
    
    __mapper_args__ = {
            "polymorphic_identity": "utilisateurs",
            "polymorphic_on": "nom"
        }
    
    client = db.relationship(
        "ClientModel", back_populates="utilisateurs", lazy=True
    )
