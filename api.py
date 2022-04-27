
from flask import Flask, jsonify, request

from flask_sqlalchemy import SQLAlchemy

api = Flask(__name__)

api.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:SecretPassw0rd@localhost:5432/save'
api.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db=SQLAlchemy(api) 

class Etudiant(db.Model):
    __tablename__='etudiants'
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    prenom = db.Column(db.String(200), nullable=False)
    adresse = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(50), unique=True)
    filiere_id = db.Column(db.Integer, db.ForeignKey('filieres.id'), nullable=False)

    # Fonction qui format en json
    # On peut passer aussi par le constructeur

    # def __init__(self, nom, prenom, adresse, email, filiere_id):
    #     self.id = isbn
    #     self.nom = titre
    #     self.prenom = date_publication
    #     self.adresse = auteur
    #     self.email = email
    #     self.filiere_id = filiere_id

    # def format_etudiant(self):
    #     return {
    #         'id': self.id,
    #         'Nom': self.nom,
    #         'Prenom' : self.prenom,
    #         'Adresse': self.adresse,
    #         'Email': self.email,
    #         'Filiere': self.filiere_id
    #     }

    # Fonction qui format en json
    # Les valeurs recus sont envoyés dans le "s" et retranscris
    def format_etudiant(s):
        return {
            'id': s.id,
            'Nom': s.nom,
            'Prenom' : s.prenom,
            'Adresse': s.adresse,
            'Email': s.email,
            'Filiere': s.filiere_id
        }
    
    # Fontion pour faire les add et commit
    def insert(s):
        db.session.add(s)
        db.session.commit()
    
    def delete(s):
        db.session.delete(s)
        db.session.commit()
    
    def update(s):
        db.session.commit()


class Filiere(db.Model):
    __tablename__='filieres'
    id = db.Column(db.Integer, primary_key=True)
    codefiliere = db.Column(db.String(50), nullable=False)
    libellefiliere = db.Column(db.String(100), nullable=False)
    etudiants = db.relationship('Etudiant', backref='filieres', lazy=True)
    
    def format_filiere(s):
        return {
            'id': s.id,
            'Code filière': s.nom,
            'Libelle filière' : s.prenom,
        }

db.create_all()
# Recuperer tous les étudiants
@api.route("/etudiants", methods=['GET']) 
def liste_etudiant():
    etudiants = Etudiant.query.all() 
    # Récupère chaque element et le format
    etudiants_format=[etudiant.format_etudiant() for etudiant in etudiants]
    return jsonify({
        'Success' : True,
        'Etudiants' : etudiants_format,
        'Nombre': len(etudiants)
    }) 

# Recuperer un étudiant
@api.route("/etudiants/<int:id>", methods=['GET']) 
def select_etudiant(id):
    etudiant = Etudiant.query.get(id) 
    return jsonify({
        'Success' : True,
        'Etudiant' : etudiant.format_etudiant()
    }) 

# Ajouter un étudiant
@api.route("/etudiants", methods=['POST'])

def enregistrer_etudiant():

    # Recupère les données envoyées en json
    body = request.get_json()

    # Recupère chaque infos sous forme json (s'assurer que le champs soit nullable pour utiliser none)
    new_nom = body.get('nom', None)
    new_prenom = body.get('prenom', None)
    new_adresse = body.get('adresse', None)
    new_email = body.get('email', None)
    new_filiere = body.get('filiere_id', None)

    # Recupère si l'id est trouvable ou pas
    filiere = Filiere.query.get(new_filiere)
    if filiere is None:
        return jsonify({
            'success':False,
            'message':'ID filière introuvable'
        })
    else :
        # Assignation des valeurs à la classe
        etudiant=Etudiant(nom=new_nom, prenom=new_prenom, adresse=new_adresse, email=new_email, filiere_id=new_filiere)

        etudiant.insert()
        # Accès aux étudiants dans la base (Un accès en une fois)
        etudiant=Etudiant.query.all()
        return jsonify ({
            'success':True,
            'etudiant_id':etudiant.id,
            'nombre': len(etudiant),
            'liste_etudiants': [etudiant.format() for e in etudiant]
        })

# Modifier un étudiant
@api.route('/etudiants/<int:id>', methods=['PATCH'])

def modifier_etudiant(id):
    etudiant=Etudiant.query.get(id)
    body=request.get_json()

    etudiant.nom = body.get('nom', None)
    etudiant.prenom = body.get('prenom', None)
    etudiant.adresse = body.get('adresse', None)
    etudiant.email = body.get('email', None)
    etudiant.filiere_id = body.get('filiere_id', None)

    etudiant.update()

    return jsonify({
        'success':True,
        'etudiant': etudiant.format_etudiant()
    })

# Supprimer un étudiant
@api.route('/etudiants/<int:id>', methods=['DELETE'])

def supprimer_etudiant(id):
    etudiant=Etudiant.query.get(id)

    etudiant.delete()

    return jsonify({
        'success':True,
        'etudiant_id': etudiant.id
    })

if __name__ == "__main__":
    api.run(debug = True)