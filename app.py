# Imporation de la librairie Flask
from flask import Flask, render_template, request

# Affectation de la fonction Flask avec "name = nom du fichier" passé en paramètre
# Transforme le fichier en une application flask
app = Flask (__name__)

@app.route("/")

# Renvoie ce fichier à l'utilisateur
def index():
# Recupère l'argument dans l'url 
    name = request.args.get("name")
# Name = variable; name = valeur
    return render_template("index.html", Name = name)

    