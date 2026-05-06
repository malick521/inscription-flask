from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.sqlite3'
app.config['SECRET_KEY'] = "random string"

data_base = SQLAlchemy(app)

class Etudiant(data_base.Model):
    id = data_base.Column(data_base.Integer, primary_key=True)
    nom = data_base.Column(data_base.String(20), nullable=False)
    email = data_base.Column(data_base.String(20), unique=True, nullable=False)
    age = data_base.Column(data_base.Integer, nullable=False)
    filiere = data_base.Column(data_base.String(5), nullable=False)
    def __init__(self,nom, email, age, filiere):
        self.nom = nom
        self.email = email
        self.age = age
        self.filiere = filiere

with app.app_context():
    data_base.create_all()

@app.route('/')
def Home():
    return render_template('home.html')   

@app.route('/add_student', methods=['GET', 'POST'])
def AddStudent():
    if request.method == 'POST':
        nom = request.form.get('nom', '').strip()
        email = request.form.get('email', '').strip()
        age = request.form.get('age', type=int)
        filiere = request.form.get('filiere')

        existing_email = Etudiant.query.filter_by(email=email).first()

        if nom == "":
            return render_template('add_student.html', error_name="Le nom ne peut pas être vide")

        if age is None or age < 0 or age < 18:
            return render_template('add_student.html', error_age="L'âge est invalide ou inaproprie")
        
        if existing_email:
            return render_template(
                'add_student.html',
                error_email="Cet email existe déjà",
            )
        
        new_etudiant = Etudiant(nom, email, age, filiere)
        data_base.session.add(new_etudiant)
        data_base.session.commit()

        return redirect('/add_student')

    return render_template('add_student.html')
 

@app.route('/listes_students')
def ListesStudent():
    etudiants = Etudiant.query.all()   
    return render_template('listes_students.html', etudiants=etudiants)  


@app.route('/contact')
def Contact():
    return render_template('contact.html')


@app.route('/delete/<int:id>')
def delete(id):
    etudiant = Etudiant.query.get(id) 
    data_base.session.delete(etudiant)
    data_base.session.commit()
    return redirect('/listes_students')

if __name__ == "__main__" :
    app.run(port=3310, debug=True)
