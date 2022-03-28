# Imporation de la librairie Flask
from flask import Flask, render_template, request

# Pour mettre des mot de passe contenant des caracrtères spéciaux et faire le formatage en gros
from urllib.parse import quote_plus

# Imporation de la bibliothèque SQLAlchemy
from flask_sqlalchemy import SQLAlchemy

# Affectation de la fonction Flask avec "name = nom du fichier" passé en paramètre (Invariable)
# Transforme le fichier en une application flask
app = Flask (__name__)

# Chaîne de connexion à la base de données
# Chemin d'accès sous ce sens => dialect://username:mypassword@localhost:portdeladb/db

passwd = quote_plus('')

app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:DeakonCYTY2000@localhost:5432/esagtest'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db=SQLAlchemy(app)

class Etudiant(db.Model):
    __tablename__='etudiants'
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    prenom = db.Column(db.String(200), nullable=False)
    adresse = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(50), unique=True)
# Relation de migration de la clé étrangère
    filiere_id = db.Column(db.Integer, db.ForeignKey('filieres.id'), nullable=False)

class Filiere(db.Model):
    __tablename__='filieres'
    id = db.Column(db.Integer, primary_key=True)
    codefiliere = db.Column(db.String(50), nullable=False)
    libellefiliere = db.Column(db.String(100), nullable=False)
    etudiants = db.relationship('Etudiant', backref='filieres', lazy=True)

class Livre(db.Model):
    __tablename__='livres'
    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(50), nullable=False)
    auteur = db.Column(db.String(50), nullable=False)
    vote = db.Column(db.Integer, nullable=True)
    datesortie = db.Column(db.DateTime, nullable=False)

db.create_all()

# @app.route("/")

# # Renvoie ce fichier à l'utilisateur
# def index():
# # Recupère l'argument dans l'url 
#     name = request.args.get("name")
# # Name = variable; name = valeur
#     return render_template("index.html", Name = name)

@app.route("/")
# Index est le controleur en quelque sorte
def index():
    etudiants = Etudiant.query.all()
    return render_template ("index.html", DataEtudiant = etudiants)

