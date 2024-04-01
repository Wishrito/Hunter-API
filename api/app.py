import os
import sqlite3

import config
from flask import Flask, jsonify, redirect, request

app = Flask(__name__)
file = './flaskTests/personnes.sqlite'



def verifier_cle_api():
    key = request.headers.get('API-Key')
    if key == config.Config().login():
        return True
    return False


@app.route('/', methods=['GET'])
def home():
    return redirect('index.html')

@app.route('/personnes', methods=['GET'])
def get_personnes():
    conn = sqlite3.connect(file)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM personnes')
    personnes = cursor.fetchall()
    conn.close()
    return jsonify(personnes)


@app.route('/personnes/<int:id>', methods=['GET'])
def get_personne(id):
    conn = sqlite3.connect(file)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM personnes WHERE id = ?', (id,))
    personne = cursor.fetchone()
    conn.close()
    if personne is None:
        return jsonify({'erreur': 'Personne non trouvée'}), 404
    return jsonify(personne)


@app.route('/personnes', methods=['POST'])
def ajouter_personne():
    if not verifier_cle_api():
        return jsonify({'erreur': 'Clé API non valide'}), 401

    donnees = request.get_json()
    if 'nom' not in donnees or 'age' not in donnees or 'ville' not in donnees:
        return jsonify({'erreur': 'Données incomplètes'}), 400

    nom = donnees['nom']
    age = donnees['age']
    ville = donnees['ville']

    conn = sqlite3.connect('personnes.sqlite')
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO personnes (nom, age, ville) VALUES (?, ?, ?)', (nom, age, ville))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Personne ajoutée avec succès'}), 201


@app.route('/personnes/search', methods=['GET'])
def recherche_personne():
    nom = request.args.get('nom')
    if nom is None:
        return jsonify({'erreur': 'Paramètre "nom" manquant'}), 400
    conn = sqlite3.connect(file)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM personnes WHERE nom = ?', (nom,))
    resultat = cursor.fetchall()
    conn.close()
    if len(resultat) == 0:
        return jsonify({'erreur': 'Aucune personne trouvée avec ce nom'}), 404
    return jsonify(resultat)


if __name__ == '__main__':

    if not os.path.exists(file):
        with open(file, "w"):
            pass

    conn = sqlite3.connect(file)
    cursor = conn.cursor()
    cursor.execute(
        '''CREATE TABLE IF NOT EXISTS personnes (id INTEGER PRIMARY KEY AUTOINCREMENT, nom TEXT, age INTEGER, ville TEXT)''')
    conn.commit()
    conn.close()
    app.run(debug=True)
