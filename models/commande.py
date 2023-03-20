from db import db

class CommandeModel(db.Model):
    __tablename__ = "commandes"

    id = db.Column(db.Integer, primary_key=True)
    date_cde = db.Column(db.DateTime, unique=True, nullable=False)
    qte_cde = db.Column(db.Integer, unique=True, nullable=False)
    #etat_cde = db.Column(db.String(40), default="En cours")
    nom_client = db.Column(db.String(40), unique=False, nullable=False)
    prenom_client = db.Column(db.String(40), unique=False, nullable=False)
    num_client = db.Column(db.String(40), unique=False, nullable=False)
    long = db.Column(db.Float, unique=True, nullable=False)
    lat = db.Column(db.Float, unique=True, nullable=False)
    
    livraisons = db.relationship(
        "LivraisonModel", back_populates="commandes", lazy=True
    )
    
    produits = db.relationship("ProduitModel", back_populates="commandes", secondary="Cde_Prods")