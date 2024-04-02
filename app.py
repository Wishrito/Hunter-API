import os
import sqlite3

from flask import Flask, redirect, render_template, request
from flask.typing import ResponseReturnValue
from werkzeug.exceptions import NotFound


class CustomFlask(Flask):
    def handle_http_exception(self, e):
        if isinstance(e, NotFound):
            return render_template('404.html'), 404
        return super().handle_http_exception(e)


app = Flask(__name__)
file = './personnes.sqlite'


def verifier_cle_api():
    key = request.headers.get('API-Key')
    if key == os.getenv("admin_key"):
        return True
    return False


@app.route('/', methods=['GET'])
def index():
    conn = sqlite3.connect(file)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM personnes')
    personnes = cursor.fetchall()

    # Liste pour stocker les résultats sous forme de dictionnaires
    results = []
    # Pour chaque ligne, créer un dictionnaire et l'ajouter à la liste
    for personne in personnes:
        # Utilisation des noms de colonnes comme clés
        # row_description contient les noms de colonnes dans l'ordre
        row_dict = {cursor.description[i][0]: value for i, value in enumerate(personne)}
        results.append(row_dict)

    return render_template('index.html', personnes=results)


@app.route('/global', methods=['GET'])
def globalMH():
    return ''


@app.route('/mh', methods=['GET'])
def firstMH():
    return {'error': 'do not call this endpoint directly !'}, 403


if __name__ == '__main__':

    # if not os.path.exists(file):
    #     with open(file, "w"):
    #         pass

    # conn = sqlite3.connect(file)
    # cursor = conn.cursor()
    # tables_requests = [
    #     'CREATE TABLE IF NOT EXISTS personnes (id INTEGER PRIMARY KEY AUTOINCREMENT, nom TEXT, prenom TEXT, age INTEGER)',
    #     'CREATE TABLE IF NOT EXISTS skills (id INTEGER PRIMARY KEY,skill1 TEXT,skill2 TEXT,skill3 TEXT,skill4 TEXT,skill5 TEXT, CONSTRAINT skills_fk FOREIGN KEY (id) REFERENCES personnes (id))'
    # ]
    # for requete in tables_requests:
    #     cursor.execute(requete)
    # conn.commit()
    # checkRequest = "SELECT nom FROM personnes WHERE nom = 'Tremion'"
    # cursor.execute(checkRequest)
    # result = cursor.fetchone()
    # conn.commit()
    # if result and result[0] == 'Tremion':
    #     pass
    # else:
    #     requete = "INSERT INTO personnes (nom, prenom, age) VALUES ('Tremion', 'Rayan', 19)"
    #     cursor.execute(requete)
    #     conn.commit()
    # conn.close()
    app.run(port=5500, debug=True)
