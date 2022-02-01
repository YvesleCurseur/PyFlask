# Pour interagir avec les bases de données par du code python
import psycopg2

# Connexion à la base de données
link = psycopg2.connect('dbname=saveus user=postgres password=DeakonCYTY2000 port=5432')

# Création du curseur pour exécuter les requêtes
cur = link.cursor()

cur.execute('DROP TABLE IF EXISTS todos;')

cur.execute(
    """
    CREATE TABLE You(
        id serial PRIMARY KEY,
        description VARCHAR NOT NULL);
    """
)

cur.execute(
    """
    INSERT INTO You(
        description) values ('Django')
    ;
    """
)

link.commit()
cur.close()
link.close()