
from .app import app, db
from flask import render_template, url_for, redirect, request
from .models import *
from .formulaires import *
from flask_wtf import FlaskForm
from wtforms import StringField,HiddenField,PasswordField
from wtforms.validators import DataRequired
from hashlib import sha256
from flask_login import login_user,current_user, login_required


@app.route("/")
def home():
    return render_template(
        "home.html",
        title="Hello World!")

@app.route("/Parterre/")
def parterre():
    return render_template(
        "parterre.html",
        mesParterre = get_parterres())


class LoginForm(FlaskForm):
    username = StringField('Username')
    password = PasswordField('Password')

    def get_authenticated_user(self):
        user = Utilisateur.query.get(self.username.data)
        if user is None:
            return None
        m = sha256()
        m.update(self.password.data.encode())
        passwd = m.hexdigest()
        return user if passwd == user.password else None

@app.route("/login/",methods=("GET","POST",))
def login():
    f = LoginForm()
    if f.validate_on_submit():
        user = f.get_authenticated_user()
        if user:
            login_user(user)
            return redirect(url_for("home"))
    return render_template(
        "login.html",
        form = f)

@app.route("/Contacts/")
def contacts():
    return render_template("contacts.html")

@app.route("/Parterre/info/<int:id>")
def parterre_info(id):
    return render_template(
        "parterre-info.html",
        parterre = get_parterre(id))

@app.route("/Capteur/")
def capteur():
    return render_template(
        "capteur.html",
        mesCapteurs = get_capteurs())

@app.route("/Capteur/info/<int:id>")
def capteur_info(id):
    return render_template("capteur-info.html",
    capteur = get_capteur_id(id))

@app.route("/Ajouter/Capteur/")
def add_Capteur():
    f = CapteurForm()
    return render_template("addCapteur.html", form = f, title= "Ajouter un nouveau Capteur")

@app.route("/Ajouter/Capteur/saving/", methods=("POST",))
def new_capteur_saving():
    """
    Saves the new capteur in the database and redirect the user to his home page.
    """
    f = CapteurForm()
    if f.validate_on_submit():
        o = Capteur(name = f.get_name(),
                    tel = f.get_phoneNumber(),
                    TypeMesure = f.get_TypeMesure(),
                    parterre = f.get_Parterre())
        db.session.add(o)
        db.session.commit()
        return redirect(url_for('capteur_info', id = o.get_id()))
    return render_template(
        "create-capteur.html",
        form  = f,
        titre = "Nouveau Capteur")

@app.route("/Supprimer/Capteur",methods=["POST","GET"])
# @login_required
def delete_capteur():
    if request.method=="POST":
        if request.form['del']=="":
            return render_template("delete-capteur.html", liste = get_capteurs(), titre="Veuillez selectionner un capteur")
        else:
            a=get_capteur_id(int(request.form['del']))
            db.session.delete(a)
            db.session.commit()
    return render_template("delete-capteur.html",liste=get_capteurs())


@app.route("/Supprimer/Capteur/<int:id>",methods=["POST","GET"])
# @login_required
def delete_cap(id=None):
    if id==None:
        if request.method=="POST":
            a=id
            db.session.delete(a)
            db.session.commit()
    else:
        capteur = get_capteur_id(id)
        db.session.delete(capteur)
        db.session.commit()
    la = get_capteurs()
    return render_template("capteur.html", mesCapteurs = la)
