import random

from extensions import db
from capteur.models import *
from graphique import Graphique, Colonne
from user.models import *
from flask.cli import with_appcontext
import click


@click.command()
@with_appcontext
def insert_data():
    # user u1
    r_admin = Role(name='admin')
    db.session.add(r_admin)
    db.session.commit()
    u1 = User(
        username='Admin',
        email="admin@localhost",
        active=1,
        password="mdp123"
    )
    u2 = User(
        username='Jason',
        email="jason@localhost",
        active=1,
        password="Neves0"
    )
    u1.roles.append(r_admin)
    db.session.add(u1)
    db.session.add(u2)
    db.session.commit()

    # capteur c1 de u1
    c1 = Capteur(
        cName='Capteur 1',
        cTel='0665925597',
        cType='Lumière',
        frequence=3,
        owner=u1,
        formule="Formule de Capteur 1"
    )
    db.session.add(c1)
    db.session.commit()

    # capteur c2 de u1
    c2 = Capteur(
        cName='Capteur 2',
        cTel='0627712403',
        cType='Pureté de l\'air',
        frequence=1,
        owner=u1,
        formule="Formule de Capteur 2"
    )
    db.session.add(c2)
    db.session.commit()

    g1=Graphique(user=u1, titre="G1")
    db.session.add(g1)

    col1 = Colonne(graphique=g1, colName="Colonne1", capteur=c1)
    db.session.add(col1)

    for a, b in enumerate(random.randint(0, 1024) for _ in range(12)):
        db.session.add(Mesure(capteur=c1, valeur=b, date=datetime.datetime.utcnow()-datetime.timedelta(days=a)))
    for a, b in enumerate(random.randint(0, 1024) for _ in range(12)):
        db.session.add(Mesure(capteur=c2, valeur=b, date=datetime.datetime.utcnow()-datetime.timedelta(days=a)))

    db.session.add(Geolocalisation(capteur=c1, position_x=47.84391,position_y=1.926951))
    db.session.add(Geolocalisation(capteur=c2, position_x=48.00000,position_y=2.000000))

    db.session.commit()
