from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///etudiants.sqlite3'
app.config['SECRET_KEY'] = "random string"

db = SQLAlchemy(app)

class Etudiant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(20), nullable=False)
    prenom = db.Column(db.String(20), nullable=False)
    matricule = db.Column(db.Integer, unique=True, nullable=False)
    specialite = db.Column(db.String(50), nullable=False)

    def __init__(self, nom, prenom, matricule, specialite):
        self.nom = nom
        self.prenom = prenom
        self.matricule = matricule
        self.specialite = specialite

# Générer la base de données et la table
with app.app_context():
    db.create_all()

@app.route('/', methods=['GET','POST'])
def Form():
    if request.method == 'POST':
        nom = request.form['nom']
        prenom = request.form['prenom']
        matricule = request.form['matricule']
        specialite = request.form['specialite']

        new_etudiant = Etudiant(nom, prenom, matricule, specialite)
        db.session.add(new_etudiant)
        db.session.commit()

        return redirect('/etudiant') 

    return render_template('inscription.html')

@app.route('/etudiant')
def liste_etudiants():
    etudiants = Etudiant.query.all()   
    return render_template('etudiant.html', etudiants=etudiants)

@app.route('/delete/<int:id>')
def delete(id):
    etudiant = Etudiant.query.get(id) 
    db.session.delete(etudiant)
    db.session.commit()
    return redirect('/etudiant')

if __name__ == "__main__":
    app.run(port=3002, debug=True)
