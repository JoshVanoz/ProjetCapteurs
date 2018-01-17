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
        title = "Capteurs")

@app.route("/Parterre/")
def parterre():
    return render_template(
        "mesParterre.html",
        mesParterre = get_parterres(),
        title       = "Liste des Parterres")

@app.route("/login/", methods = ("GET","POST",))
def login():
	f = LoginForm()
	if not f.is_submitted():
		f.set_next(request.args.get("next"))
	elif f.validate_on_submit():
		user = f.get_authenticated_user()
		if user:
			login_user(user)
			next = f.get_next() or url_for("home")
			return redirect(next)
	return render_template(
        "login.html",
        form  = f,
        title = "Connexion")

@app.route("/inscription/", methods = ("GET","POST",))
def inscription():
    f = InscriptionForm()
    return render_template(
        "inscription.html",
        form = f,
        title = "Inscription")

@app.route("/inscription/save/", methods=["POST"])
def save_inscription():
    user = None
    f = InscriptionForm()
    if f.validate_on_submit() and f.uniq_Username() and f.passwd_confirmed():
        from hashlib import sha256
        m = sha256()
        m.update(f.get_mdp().encode())
        user = Utilisateur(
            idU     = f.get_id(),
            mdpU    = m.hexdigest(),
            nomU    = f.get_name(),
            prenomU = f.get_surname())
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template(
		"inscription.html",
		form  = f,
        title = "Inscription")

@app.route("/logout/")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/Contacts/")
def contacts():
    return render_template(
        "contacts.html",
        title = "Contacts")

@app.route("/Parterre/info/<int:id>")
def parterre_info(id):
    parterre = get_parterre(id)
    return render_template(
        "parterre-info.html",
        parterre = parterre,
        title    = parterre.get_name())

@app.route("/Capteur/")
def capteur():
    return render_template(
        "capteur.html",
        mesCapteurs = get_capteurs(),
        title = "Liste des Capteurs")


@app.route("/Capteur/info/<int:id>")
def capteur_info(id):
    capteur = get_capteur(id)
    return render_template(
        "capteur-info.html",
        capteur  = capteur,
        title    = capteur.get_name(),
        parterre = get_parterre(capteur.get_parterre()),
        mesure   = get_typeMesure(capteur.get_typeMesure()))

@app.route("/Ajouter/Capteur/")
@login_required
def add_Capteur():
    f = CapteurForm()
    return render_template(
        "addCapteur.html",
        form  = f,
        title = "Nouveau Capteur")

@app.route("/Ajouter/Capteur/saving/", methods=("POST",))
def new_capteur_saving():
    """
    Saves the new capteur in the database and redirect the user to his home page.
    """
    f = CapteurForm()
    if f.validate_on_submit():
        o = Capteur(
            name       = f.get_name(),
            intervalle = f.get_interval(),
            tel        = f.get_phoneNumber(),
            TypeMesure = f.get_typeMesure().get_id(),
            parterre   = f.get_parterre().get_id())
        db.session.add(o)
        db.session.commit()
        return redirect(url_for('capteur_info', id = o.get_id()))
    return render_template(
        "addCapteur.html",
        form  = f,
        titre = "Nouveau Capteur")

@app.route("/Supprimer/Capteur", methods = ["POST","GET"])
@login_required
def delete_capteur():
    if request.method=="POST":
        if request.form['del']=="":
            return render_template(
                "delete-capteur.html",
                liste = get_capteurs(),
                title = "Supprimer un capteur")
        else:
            a = get_capteur(int(request.form['del']))
            db.session.delete(a)
            db.session.commit()
    return render_template(
        "delete-capteur.html",
        liste = get_capteurs(),
        title = "Supprimer un capteur")


@app.route("/Supprimer/Capteur/<int:id>")
@login_required
def delete_cap(id):
    capteur = get_capteur(id)
    db.session.delete(capteur)
    db.session.commit()
    return redirect(url_for("capteur"))


@app.route("/Ajouter/Parterre/")
@login_required
def add_Parterre():
    f = ParterreForm()
    return render_template(
        "create-parterre.html",
        form  = f,
        title = "Ajouter un nouveau Parterre")

@app.route("/Ajouter/Parterre/saving/", methods=("POST",))
def new_parterre_saving():
    f = ParterreForm()
    if f.validate_on_submit():
        o = Parterre(name = f.get_name())
        db.session.add(o)
        form = request.form
        longitudes = form.getlist("longitudes")
        latitudes  = form.getlist("latitudes")
        num = 0
        for longitude,latitude in zip(longitudes, latitudes):
            c = Coordonnees(x        = longitude,
                            y        = latitude,
                            parterre = o.get_id(),
                            num      = num)
            num = num+1
            try:
                o.add_coordonnee(c)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
        db.session.commit()
        return redirect(url_for('parterre_info', id = o.get_id()))
    return render_template(
        "create-parterre.html",
        form  = f,
        titre = "Nouveau Capteur")

@app.route("/Capteur/edit/<int:id>")
def edit_capteur(id):
    capteur = get_capteur(id)
    form = CapteurForm(capteur)
    return render_template(
        "addCapteur.html",
        title = capteur.get_name()+" - edit",
        form  = form)

@app.route("/Capteur/save/", methods = ("POST",))
def save_capteur():
    f = CapteurForm()
    a = get_capteur(f.get_id())
    if f.validate_on_submit():
        a.set_name(f.get_name())
        a.set_num(f.get_phoneNumber())
        a.set_interval(f.get_interval())
        if a.get_parterre() != f.get_parterre().get_id():
            a.set_parterre(f.get_parterre().get_id())
        if a.get_typeMesure() != f.get_typeMesure().get_id():
            a.set_typeMesure(f.get_typeMesure().get_id())
        db.session.commit()
        return redirect(url_for(
            "capteur_info",
            id    = f.get_id()))
    return render_template(
        "addCapteur.html",
        title = a.get_name()+" - edit",
        form  = f)

@app.route("/Parterre/edit/<int:id>")
def edit_parterre(id):
    parterre = get_parterre(id)
    form = ParterreForm(parterre)
    return render_template("create-parterre.html",
                title= parterre.get_name()+"  - edit",
                form = form)

@app.route("/Parterre/save/", methods = ("POST",))
def save_parterre():
    f= ParterreForm()
    a = get_parterre(f.get_id())
    if f.validate_on_submit():
        a.set_name(f.get_name())
        a.remove_coordonnees()
        db.session.commit()
        form = request.form
        longitudes = form.getlist("longitudes")
        latitudes  = form.getlist("latitudes")
        num = 0
        for longitude,latitude in zip(longitudes, latitudes):
            c = Coordonnees(x        = longitude,
                            y        = latitude,
                            parterre = a.get_id(),
                            num      = num)
            num = num+1
            a.add_coordonnee(c)
        db.session.commit()
        return redirect(url_for("parterre_info", id = a.get_id()))
    return render_template("create-parterre.html",
                title= parterre.get_name()+"  - edit",
                form = f)

@app.route("/Supprimer/Parterre/<int:id>")
def delete_parterre(id):
    a   = get_parterre(id)
    bac = get_bac_a_sable()
    for capteur in a.get_capteurs():
        capteur.set_parterre(bac.get_id())
    db.session.delete(a)
    db.session.commit()
    return redirect(url_for("parterre"))
