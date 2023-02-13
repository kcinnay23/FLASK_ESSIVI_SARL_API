from db import db
from models import utilisateur

class AdminModel(utilisateur):
    __tablename__ = 'admins'

    id = db.Column(db.Integer, db.ForeignKey("utilisateurs.id"), primary_key=True)
    
    __mapper_args__ = {
        "polymorphic_identity": "admins"
    }