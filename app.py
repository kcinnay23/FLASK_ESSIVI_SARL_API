import os
from flask import Flask, jsonify
from flask_smorest import Api
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
import secrets


import models

from db import db
from resources.client import blp as ClientBlueprint
from resources.commande import blp as CommandeBlueprint
from resources.depot import blp as DepotBlueprint
from resources.livraison import blp as LivraisonBlueprint
from resources.produit import blp as ProduitBlueprint
from resources.utilisateur import blp as UtilisateurBlueprint
from resources.administrateur import blp as AdministrateurtBlueprint


def create_app(db_url=None):
    app = Flask(__name__)
    app.config["API_TITLE"] = "Essivi_Sarl REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config[
        "OPENAPI_SWAGGER_UI_URL"
    ] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    # app.config["SQLALCHEMY_DATABASE_URI"] = db_url or "sqlite:///data.db"
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:root@localhost:5432/essivi'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/essivi'

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["PROPAGATE_EXCEPTIONS"] = True
    
    db.init_app(app)
    
    migrate = Migrate(app, db)
    
    api = Api(app)
    
    #app.config["JWT_SECRET_KEY"] = "235373032930652279442321549971329156695"
    app.config["JWT_SECRET_KEY"] = "Yann"
    jwt = JWTManager(app)
    
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return (
            jsonify({"message": "The token has expired.", "error": "token_expired"}),
            401,
        )

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return (
            jsonify(
                {"message": "Signature verification failed.", "error": "invalid_token"}
            ),
            401,
        )

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return (
            jsonify(
                {
                    "description": "Request does not contain an access token.",
                    "error": "authorization_required",
                }
            ),
            401,
        )

    @jwt.needs_fresh_token_loader
    def token_not_fresh_callback(jwt_header, jwt_payload):
        return (
            jsonify(
                {
                    "description": "The token is not fresh.",
                    "error": "fresh_token_required",
                }
            ),
            401,
        )

    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return (
            jsonify(
                {"description": "The token has been revoked.", "error": "token_revoked"}
            ),
            401,
        )

    with app.app_context():
        db.create_all()

    api.register_blueprint(ClientBlueprint)
    api.register_blueprint(CommandeBlueprint)
    api.register_blueprint(DepotBlueprint)
    api.register_blueprint(LivraisonBlueprint)
    api.register_blueprint(ProduitBlueprint)
    api.register_blueprint(UtilisateurBlueprint)
    api.register_blueprint(AdministrateurtBlueprint)


    return app
