# Imporation de la librairie Flask
from flask import Flask, redirect, render_template, request, url_for

# Pour mettre des mot de passe contenant des caracrtères spéciaux et faire le formatage en gros
from urllib.parse import quote_plus

# Imporation de la bibliothèque SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
from ray import method

# Affectation de la fonction Flask avec "name = nom du fichier" passé en paramètre (Invariable)
# Transforme le fichier en une application flask
app = Flask (__name__)

# Chaîne de connexion à la base de données
# Chemin d'accès sous ce sens => dialect://username:mypassword@localhost:portdeladb/db

passwd = quote_plus('')

app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:SecretPassw0rd@localhost:5432/save'
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

# Route fonction qui appel lafonction index
@app.route("/etudiants") # 1
# Index est le controleur en quelque sorte
def index():
    etudiants = Etudiant.query.all() #2 - 3
    return render_template ("index.html", dataEtudiant = etudiants) # 4


@app.route("/etudiants/create", methods = ['POST', 'GET'])
def createform():
    if request.method == 'GET':

        filieres = Filiere.query.all() 
        return render_template('create.html', dataFiliere = filieres)

    elif request.method == 'POST':
        vfiliere = request.form.get('filiere_select')
        vnom = request.form.get('nom')
        vprenom = request.form.get('prenom')
        vadresse = request.form.get('adresse')
        vemail = request.form.get('email')

        oneEtudiant = Etudiant(nom = vnom, prenom = vprenom, adresse=vadresse, email=vemail, filiere_id=vfiliere)   
        
        db.session.add(oneEtudiant)
        db.session.commit()
        return redirect(url_for('createform'))

if __name__ == "__main__":
    app.run(debug = True)