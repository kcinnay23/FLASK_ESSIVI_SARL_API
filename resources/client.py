from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from db import db
from models import ClientModel
from schemas import ClientSchema, ClientUpdateSchema

blp = Blueprint("Clients", "clients", description="Opérations sur les clients")


@blp.route("/client/<int:client_id>")
class Client(MethodView):
    @blp.response(200, ClientSchema)
    # Récuperer un client
    def get(self, client_id):
        client = ClientModel.query.get_or_404(client_id)
        return client

    # Supprimer un client
    def delete(self, client_id):
        Client = ClientModel.query.get_or_404(client_id)
        db.session.delete(Client)
        db.session.commit()
        return {"message": "Client deleted."}

    @blp.arguments(ClientUpdateSchema)
    @blp.response(200, ClientSchema)
    # Modifier un client
    def put(self, Client_data, client_id):
        Client = ClientModel.query.get(client_id)

        if Client:
            Client.nom = Client_data["nom"]
            Client.prenom = Client_data["prenom"]
            Client.numTel = Client_data["numTel"]
            Client.adresse = Client_data["adresse"]
        else:
            Client = ClientModel(id=client_id, **Client_data)

        db.session.add(Client)
        db.session.commit()

        return Client


@blp.route("/client")
class ClientList(MethodView):
    @blp.response(200, ClientSchema(many=True))
    # Récuperer tout les clients
    def get(self):
        return ClientModel.query.all()

    @blp.arguments(ClientSchema)
    @blp.response(201, ClientSchema)
    # Ajouter un client
    def post(self, client_data):
        client = ClientModel(**client_data)
        try:
            db.session.add(client)
            db.session.commit()
        except IntegrityError:
            abort(
                400,
                message="A client with that name already exists.",
            )
        except SQLAlchemyError:
            abort(500, message="An error occurred creating the client.")

        if not isinstance(client, ClientModel):
            abort(500, message="Client was not created correctly.")
        
        return client








