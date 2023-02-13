from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError

from db import db
from models import LivraisonModel
from schemas import LivraisonSchema

blp = Blueprint("Livraisons", "livraisons", description="Operations sur les livraisons")


@blp.route("/livraison/<string:livraison_id>")
class Livraison(MethodView):
    @blp.response(200, LivraisonSchema)
    #Ajouter une livraison
    def get(self, livraison_id):
        livraison = LivraisonModel.query.get_or_404(livraison_id)
        return livraison

    """Supprimer une livraison
    def delete(self, livraison_id):
        livraison = LivraisonModel.query.get_or_404(livraison_id)
        db.session.delete(livraison)
        db.session.commit()
        return {"message": "Livraison deleted."}"""

@blp.route("/livraison")
class LivraisonList(MethodView):
    @blp.response(200, LivraisonSchema(many=True))
    #Afficher une livraison
    def get(self):
        return LivraisonModel.query.all()

    @blp.arguments(LivraisonSchema)
    @blp.response(201, LivraisonSchema)
    #Ajouter une livraison
    def post(self, livraison_data):
        livraison = LivraisonModel(**livraison_data)

        try:
            db.session.add(livraison)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the livraison.")

        return livraison
