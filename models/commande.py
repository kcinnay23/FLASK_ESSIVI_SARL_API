from db import db

class CommandeModel(db.Model):
    __tablename__ = "commandes"

    id = db.Column(db.Integer, primary_key=True)
    date_cde = db.Column(db.DateTime, unique=True, nullable=False)
    qte_cde = db.Column(db.Integer, unique=True, nullable=False)
    etat_cde = db.Column(db.String(40), default="En cours")
    
    livraison = db.relationship(
        "LivraisonModel", back_populates="Commandes", lazy=True
    )
    
    produit = db.relationship("ProduitModel", back_populates="commandes", secondary="Cde_Prods")