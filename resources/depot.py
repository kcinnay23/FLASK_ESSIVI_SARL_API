from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from db import db
from models import DepotModel
from schemas import DepotSchema


blp = Blueprint("Depots", "depots", description="Operations sur les dépôts")


@blp.route("/depot/<string:depot_id>")
class Depot(MethodView):
    @blp.response(200, DepotSchema)
    #Afficher un dépôt
    def get(self, depot_id):
        depot = DepotModel.query.get_or_404(depot_id)
        return depot
    
    """Supprimer un dépôt
    def delete(self, depot_id):
        depot = DepotModel.query.get_or_404(depot_id)
        db.session.delete(depot)
        db.session.commit()
        return {"message": "Depot deleted"}, 200"""

@blp.route("/depot")
class DepotList(MethodView):
    @blp.response(200, DepotSchema(many=True))
    #Afficher tout dépôt
    def get(self):
        return DepotModel.query.all()

    @blp.arguments(DepotSchema)
    @blp.response(201, DepotSchema)
    #Ajouter un dépôt
    def post(self, depot_data):
        depot = DepotModel(**depot_data)
        try:
            db.session.add(depot)
            db.session.commit()
        except IntegrityError:
            abort(
                400,
                message="A depot with that name already exists.",
            )
        except SQLAlchemyError:
            abort(500, message="An error occurred creating the depot.")

        return depot
