from flask import jsonify, request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    jwt_required,
)
from passlib.hash import pbkdf2_sha256

from db import db
from models import UtilisateurModel
from models.administrateur import AdminModel
from models.distributeur import DistributeurModel
from schemas import UtilisateurSchema

blp = Blueprint("Utilisateurs", "utilisateurs", description="Operations on users")


@blp.route("/register")
class UserRegister(MethodView):
    @blp.arguments(UtilisateurSchema)
    def post(self, user_data):
        if UtilisateurModel.query.filter(UtilisateurModel.username == user_data["username"]).first():
            abort(409, message="A user with that username already exists.")

        user = UtilisateurModel(
            nom = user_data["nom"],
            prenom = user_data["prenom"],
            numTel = user_data["numTel"],
            username = user_data["username"],
            password=pbkdf2_sha256.hash(user_data["password"]),
            roles = user_data["roles"]
        )
        if user.roles == 'administrateur':
            user = AdminModel(
                nom=user.nom, 
                prenom=user.prenom, 
                numTel=user.numTel, 
                username=user.username,
                password=pbkdf2_sha256.hash(user_data["password"]))
            
        elif user.roles == 'distributeur':
            user = DistributeurModel(
                nom=user.nom,
                prenom=user.prenom,
                numTel=user.numTel,
                username=user.username,
                password=pbkdf2_sha256.hash(user_data["password"]),
                code_agent=user_data.get("code_agent"),
                plaque_voiture=user_data.get("plaque_voiture"))
        else:
            user = UtilisateurModel(nom=user.nom, prenom=user.prenom, numTel=user.numTel, username=user.username,
                             password=pbkdf2_sha256.hash(user_data["password"]), roles=user.roles)

        db.session.add(user)
        db.session.commit()

        return {"message": "User created successfully."}, 200

@blp.route("/login")
class UserLogin(MethodView):
    @blp.arguments(UtilisateurSchema(only=["username", "password"]))
    def post(self, user_data):
        user = UtilisateurModel.query.filter(
            UtilisateurModel.username == user_data["username"]
        ).first()

        if user and pbkdf2_sha256.verify(user_data["password"], user.password):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return {"access_token": access_token, "refresh_token": refresh_token}, 200

        abort(401, message="Invalid credentials.")

@blp.route("/logout")
class UserLogout(MethodView):
    @jwt_required()
    def post(self):
        #jti = get_jwt()["jti"]
        #BLOCKLIST.add(jti)
        return {"message": "Successfully logged out"}, 200


@blp.route("/user/<int:user_id>")
class User(MethodView):
    """
    This resource can be useful when testing our Flask app.
    We may not want to expose it to public users, but for the
    sake of demonstration in this course, it can be useful
    when we are manipulating data regarding the users.
    """

    @blp.response(200, UtilisateurSchema)
    def get(self, user_id):
        user = UtilisateurModel.query.get_or_404(user_id)
        return user

    def delete(self, user_id):
        user = UtilisateurModel.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return {"message": "User deleted."}, 200


@blp.route("/refresh")
class TokenRefresh(MethodView):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        # Make it clear that when to add the refresh token to the blocklist will depend on the app design
        #jti = get_jwt()["jti"]
        #BLOCKLIST.add(jti)
        return {"access_token": new_token}, 200
    
@blp.route("/utilisateur")
class UtilisateurList(MethodView):
    @blp.response(200, UtilisateurSchema(many=True))
    # Afficher les utilisateurs
    def get(self):
        return UtilisateurModel.query.all()
