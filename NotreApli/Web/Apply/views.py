from .app import app, db
from flask import render_template, url_for, redirect, request
from .models import *
from .formulaires import *
from flask_wtf import FlaskForm
from wtforms import StringField,HiddenField,PasswordField
from wtforms.validators import DataRequired
from flask_login import login_user,current_user, logout_user, login_required

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

@app.route("/login/",methods=("GET","POST",))
def login():
	f= UserForm()
	if not f.is_submitted():
		f.next.data = request.args.get("next")
	elif f.validate_on_submit():
		user = f.get_authenticated_user()
		if user:
			login_user(user)
			next = f.next.data or url_for("home")
			return redirect(next)
	return render_template("login.html",form=f)

@app.route("/inscription/",methods=("GET","POST",))
def inscription():
    f=InscriptionForm()
    return render_template("inscription.html",form=f)

@app.route("/inscription/save/", methods=["POST"])
def save_inscription():
    user= None
    f=InscriptionForm()
    from hashlib import sha256
    m = sha256()
    m.update(f.password.data.encode())
    if f.validate_on_submit():
        user=Utilisateur(idU=f.username.data,mdpU=m.hexdigest(),nomU=f.nom.data,prenomU=f.prenom.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template(
		"inscription.html",
		form=f)

@app.route("/logout/")
def logout():
    logout_user()
    return redirect(        "create-capteur.html",
url_for('home'))

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
@login_required
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
                    parterre = f.get_Parterre(),
                    x = f.get_coordonnees()[0],
                    y = f.get_coordonnees()[1],
                    intervalle = f.get_interval())
        db.session.add(o)
        db.session.commit()
        return redirect(url_for('capteur_info', id = o.get_id()))
    return render_template(
        "addCapteur.html",
        form  = f,
        titre = "Nouveau Capteur")

@app.route("/Supprimer/Capteur",methods=["POST","GET"])
@login_required
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
@login_required
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


@app.route("/Ajouter/Parterre/")
@login_required
def add_Parterre():
    f = ParterreForm()
    return render_template("create-parterre.html", form = f, title= "Ajouter un nouveau Parterre")

@app.route("/Ajouter/Parterre/saving/", methods=("POST",))
def new_parterre_saving():
    f = ParterreForm()
    if f.validate_on_submit():
        o = Parterre(nomP = f.get_name(),
                    lieuGeoPX = f.get_lieuGeoPx(),
                    lieuGeoPY = f.get_lieuGeoPy())
        db.session.add(o)
        db.session.commit()
        return redirect(url_for('parterre_info', id = o.get_id()))
    return render_template(
        "create-parterre.html",
        form  = f,
        titre = "Nouveau Capteur")

@app.route("/Capteur/edit/<int:id>")
def edit_capteur(id):
    capteur = get_capteur_id(id)
    form = CapteurForm(capteur)
    return render_template(
        "addCapteur.html",
        titre = capteur.get_name(),
        form=form)

@app.route("/Capteur/save/<int:id>")
def save_capteur(id):
    pass
    # f = CapteurForm()
    # a = get_capteur_id(id)
    # a.set_name(f.get_name())
    # a.set
