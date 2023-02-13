from flask import Flask
from flask_smorest import Api

import models

from db import db
from resources.client import blp as ClientBlueprint
from resources.commande import blp as CommandeBlueprint
from resources.depot import blp as DepotBlueprint
from resources.livraison import blp as LivraisonBlueprint
from resources.produit import blp as ProduitBlueprint


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
    #app.config["SQLALCHEMY_DATABASE_URI"] = db_url or "sqlite:///data.db"
    #app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:root@localhost:5432/essivi'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/essivi'

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["PROPAGATE_EXCEPTIONS"] = True
    db.init_app(app)
    api = Api(app)

    with app.app_context():
        db.create_all()

    api.register_blueprint(ClientBlueprint)
    api.register_blueprint(CommandeBlueprint)
    api.register_blueprint(DepotBlueprint)
    api.register_blueprint(LivraisonBlueprint)
    api.register_blueprint(ProduitBlueprint)

    return app
