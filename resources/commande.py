from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError

from db import db
from models import CommandeModel
from schemas import CommandeSchema, CommandeUpdateSchema

blp = Blueprint("Commandes", "commandes",
                description="Operations sur les commandes")


@blp.route("/commande/<string:commande_id>")
class Commande(MethodView):
    @blp.response(200, CommandeSchema)
    # Afficher une commmande
    def get(self, commande_id):
        commande = CommandeModel.query.get_or_404(commande_id)
        return commande

    """Supprimer une commande
    def delete(self, commande_id):
        commande = CommandeModel.query.get_or_404(commande_id)
        db.session.delete(commande)
        db.session.commit()
        return {"message": "Commande deleted."}"""

    # @blp.arguments(CommandeUpdateSchema)
    # @blp.response(200, CommandeSchema)
    # Modifier une commmande
    # def put(self, commande_data, commande_id):
    #    commande = CommandeModel.query.get(commande_id)

    #    if commande:
    #        commande.qte_cde = commande_data["qte_cde"]
    #    else:
    #        commande = CommandeModel(id=commande_id, **commande_data)

    #    db.session.add(commande)
    #    db.session.commit()

    #    return commande


@blp.route("/commande")
class CommandeList(MethodView):
    @blp.response(200, CommandeSchema(many=True))
    # Afficher tout les commmandes
    def get(self):
        return CommandeModel.query.all()

    @blp.arguments(CommandeSchema)
    @blp.response(201, CommandeSchema)
    # Ajouter une commmandes
    def post(self, commande_data):
        commande = CommandeModel(**commande_data)

        try:
            db.session.add(commande)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the commande.")

        return commande
