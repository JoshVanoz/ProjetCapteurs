from flask import Blueprint,request, jsonify, redirect, url_for
from flask.ext.login import login_required

from extensions import db
from flask.templating import render_template
from .models import Capteur, get_capteur, Mesure, Geolocalisation
from flask_security import current_user

bp_capteur = Blueprint('capteur_bp',__name__, static_folder='../static')

@bp_capteur.route('/principale',methods=('GET', 'POST'))
def principale():
    if current_user.is_authenticated:
        if request.method=="POST" and "add" in request.form:
            c=Capteur(
                cName=request.form["nom"],
                cTel=request.form["numeroTel"],
                cType=request.form["type"],
                frequence=request.form["frequence"],
                owner=current_user,
                formule=request.form["formule"]
            )
            db.session.add(c)
            db.session.commit()
        else:
            if request.method=="POST" and "suppression" in request.form:
                db.session.delete(get_capteur(request.form["numero"]))
                db.session.commit()
            else:
                if request.method=="POST" and "validation" in request.form:
                    c=get_capteur(request.form["numero"])
                    c.cName=request.form["nom"]
                    c.cType=request.form["type"]
                    c.frequence=request.form["frequence"]
                    c.owner=current_user
                    c.formule=request.form["formule"]
                    db.session.add(c)
                    db.session.commit()
        return render_template('principale.html',listeCapteurs=Capteur.query.all(),size=len(Capteur.query.all()))
    else:
        return redirect(url_for('public.index'))


@bp_capteur.route("/measure/<sender>/<value>")
def measure(sender, value):
    c = Capteur.query.filter_by(cTel=sender).first()
    if not c:
        return "Envoyeur Inconnu."
    m = Mesure(capteur=c,
               valeur=value)
    db.session.add(m)
    db.session.commit()
    return "Succès."


@bp_capteur.route("/position/<sender>/<value>")
def position(sender, value):
    c = Capteur.query.filter_by(cTel=sender).first()
    if not c:
        return "Envoyeur Inconnu."
    x, y = value.split(';')
    try:
        x = float(x)
        y = float(y)
    except ValueError:
        return "Posiontion non-flottante."
    m = Geolocalisation(capteur=c,
                        position_x=x,
                        position_y=y)
    db.session.add(m)
    db.session.commit()
    return "Succès."



@bp_capteur.route("/api/capteurs")
def capteurs():
    return jsonify([o.serialize() for o in Capteur.query.all() if len(o.positions.all()) > 0])
