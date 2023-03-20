from marshmallow import Schema, fields


class PlainClientSchema(Schema):
    id = fields.Int(dump_only=True)
    nom = fields.Str(required=True)
    prenom = fields.Str(required=True)
    numTel = fields.Str(required=True)
    adresse = fields.Str(required=True)


class PlainDepotSchema(Schema):
    id = fields.Int(dump_only=True)
    nom = fields.Str(required=True)
    long = fields.Float(required=True)
    lat = fields.Float(required=True)


class PlainCommandeSchema(Schema):
    id = fields.Int(dump_only=True)
    date_cde = fields.DateTime(required=True)
    qte_cde = fields.Int(required=True)
    #etat_cde = fields.Str()
    nom_client = fields.Str()
    prenom_client = fields.Str()
    num_client = fields.Str()
    long = fields.Str()
    lat = fields.Str()


class PlainLivraisonSchema(Schema):
    id = fields.Int(dump_only=True)
    date_Livraison = fields.DateTime(required=True)
    #qte_Livree = fields.Int(required=True)
    montant = fields.Float(required=True)
    #etat_Livraison = fields.Str(required=True)
    #remise = fields.Float(required=True)
    #montant_remise = fields.Float(required=True)
    #montant_Final = fields.Float(required=True)
    
    
class PlainUtilisateurSchema(Schema):
    id = fields.Int(dump_only=True)
    nom = fields.Str(required=True)
    prenom = fields.Str(required=True)
    numTel = fields.Str(required=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True)
    roles = fields.Str(required=True)
    code_agent = fields.Str()
    plaque_voiture = fields.Str()


class PlainProduitSchema(Schema):
    id = fields.Int(dump_only=True)
    libelle_prod = fields.Str(required=True)
    prix_unitaire = fields.Float(required=True)
    url = fields.Str(required=True)
    
class ClientSchema(PlainClientSchema):
    utilisateur_id = fields.Int(required=True, load_only=True)
    
    utilisateurs = fields.Nested(PlainUtilisateurSchema(), dump_only=True)
    
    depots = fields.List(fields.Nested(PlainDepotSchema()), dump_only=True)


class DistributeurSchema(Schema):
    id = fields.Int(required=True, load_only=True)
    code_agent = fields.Str(required=True)
    plaque_agent = fields.Int(required=True)
    utilisateurs = fields.List(fields.Nested(PlainUtilisateurSchema()), dump_only=True)
    livraisons = fields.List(fields.Nested(PlainLivraisonSchema()), dump_only=True)
    
class AdministrateurSchema(PlainUtilisateurSchema):
    id = fields.Int(required=True, load_only=True)
    utilisateurs = fields.List(fields.Nested(PlainUtilisateurSchema()), dump_only=True)
    


class CommandeSchema(PlainCommandeSchema):
    livraisons = fields.List(fields.Nested(PlainLivraisonSchema()), dump_only=True)
    produits = fields.Nested(PlainProduitSchema(), dump_only=True)


class DepotSchema(PlainDepotSchema):
    client_id = fields.Int(required=True, load_only=True)
    client = fields.List(fields.Nested(PlainClientSchema()), dump_only=True)


class LivraisonSchema(PlainLivraisonSchema):
    distributeur_id = fields.Int(required=True, load_only=True)
    commande_id = fields.Int(required=True, load_only=True)
    commande = fields.List(fields.Nested(PlainCommandeSchema()), load_only=True)
    distributeur = fields.List(fields.Nested(PlainClientSchema()), dump_only=True)


class ProduitSchema(PlainProduitSchema):
    Commande = fields.Nested(PlainCommandeSchema(), dump_only=True)


class UtilisateurSchema(PlainUtilisateurSchema):
    Client = fields.List(fields.Nested(PlainClientSchema()), dump_only=True)


class CommandeAndProduitSchema(Schema):
    message = fields.Str()
    commande = fields.Nested(CommandeSchema)
    produit = fields.Nested(ProduitSchema)


class ProduitUpdateSchema(Schema):
    libelle_prod = fields.Str()
    prix_unitaire = fields.Float()
    url = fields.Str()


class DepotUpdateSchema(Schema):
    nom = fields.Str()
    long = fields.Float()
    lat = fields.Float()


class ClientUpdateSchema(Schema):
    nom = fields.Str()
    prenom = fields.Str()
    numTel = fields.Str()
    adresse = fields.Str()


class CommandeUpdateSchema(Schema):
    qte_cde = fields.Int()
