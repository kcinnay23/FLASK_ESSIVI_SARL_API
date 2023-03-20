from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from db import db
from models import ProduitModel, CommandeModel
from schemas import ProduitSchema, CommandeAndProduitSchema

blp = Blueprint("Produits", "produits", description="Operations les produits")


@blp.route("/commande/<int:commande_id>/produit/<int:produit_id>")
class LinkCommandesToProduit(MethodView):
    @blp.response(201, ProduitSchema)
    # Afficher un produit d'une commande
    def post(self, commande_id, produit_id):
        commande = CommandeModel.query.get_or_404(commande_id)
        produit = ProduitModel.query.get_or_404(produit_id)

        commande.produits.append(produit)

        try:
            db.session.add(commande)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the produit.")

        return produit

    @blp.response(200, CommandeAndProduitSchema)
    # Supprimer un produit d'une commande
    def delete(self, commande_id, produit_id):
        commande = CommandeModel.query.get_or_404(commande_id)
        produit = ProduitModel.query.get_or_404(produit_id)

        commande.produits.remove(produit)

        try:
            db.session.add(commande)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the produit.")

        return {"message": "Produit removed from produit", "commande": commande, "produit": produit}


@blp.route("/produit/<int:produit_id>")
class Tag(MethodView):
    @blp.response(200, ProduitSchema)
    # Récupérer un produit
    def get(self, produit_id):
        produit = ProduitModel.query.get_or_404(produit_id)
        return produit

    @blp.response(
        202,
        description="Deletes a produit if no commande is produitged with it.",
        example={"message": "Tag deleted."},
    )
    @blp.alt_response(404, description="Produit not found.")
    @blp.alt_response(
        400,
        description="Returned if the produit is assigned to one or more commandes. In this case, the produit is not deleted.",
    )
    # Supprimer un produit
    def delete(self, produit_id):
        produit = ProduitModel.query.get_or_404(produit_id)

        if not produit.commandes:
            db.session.delete(produit)
            db.session.commit()
            return {"message": "Tag deleted."}
        abort(
            400,
            message="Could not delete produit. Make sure produit is not associated with any commandes, then try again.",  # noqa: E501
        )


@blp.route("/produit")
class ProduitList(MethodView):
    @blp.response(200, ProduitSchema(many=True))
    # Afficher les produits
    def get(self):
        return ProduitModel.query.all()

    @blp.arguments(ProduitSchema)
    @blp.response(201, ProduitSchema)
    # Ajouter un produit
    def post(self, produit_data):
        produit = ProduitModel(**produit_data)
        try:
            db.session.add(produit)
            db.session.commit()
        except IntegrityError:
            abort(
                400,
                message="A produit with that name already exists.",
            )
        except SQLAlchemyError:
            abort(500, message="An error occurred creating the produit.")

        return produit
