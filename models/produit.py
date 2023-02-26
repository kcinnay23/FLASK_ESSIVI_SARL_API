from db import db


class ProduitModel(db.Model):
    __tablename__ = "produits"

    id = db.Column(db.Integer, primary_key=True)
    libelle_prod = db.Column(db.String(40), unique=True, nullable=False)
    prix_unitaire = db.Column(db.Float, unique=False, nullable=False)
    url = db.Column(db.String(80), unique=True, nullable=False)

    commandes = db.relationship(
        "CommandeModel", back_populates="produits", secondary="Cde_Prods")
