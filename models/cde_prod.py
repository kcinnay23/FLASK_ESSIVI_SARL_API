from db import db


class Cde_Prod(db.Model):
    __tablename__ = "Cde_Prods"

    id = db.Column(db.Integer, primary_key=True)
    commande_id = db.Column(db.Integer, db.ForeignKey("commandes.id"))
    produit_id = db.Column(db.Integer, db.ForeignKey("produits.id"))
