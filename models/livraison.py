from db import db


class LivraisonModel(db.Model):
    __tablename__ = "livraisons"

    id = db.Column(db.Integer, primary_key=True)
    date_Livraison = db.Column(db.DateTime, unique=True, nullable=False)
    qte_Livree = db.Column(db.Integer, unique=False, nullable=False)
    montant = db.Column(db.Float, unique=True, nullable=False)
    etat_Livraison = db.Column(db.String(40), unique=True, nullable=False)
    remise = db.Column(db.Float, unique=False, nullable=False)
    montant_remise = db.Column(db.Float, unique=True, nullable=False)
    montant_Final = db.Column(db.Float, unique=True, nullable=False)

    distributeur_id = db.Column(
        db.Integer, db.ForeignKey("distributeurs.id"), unique=False, nullable=False
    )
    
    distributeurs = db.relationship("DistributeurModel", back_populates="livraisons")


    commande_id = db.Column(
        db.Integer, db.ForeignKey("commandes.id"), unique=False, nullable=False
    )

    commandes = db.relationship("CommandeModel", back_populates="livraisons")
