
from .app import manager, db
from datetime import datetime

@manager.command
def loaddb():
    from .models import Coordonnees, Utilisateur, Parterre, TypePlante, TypeMesure, Capteur, AlesDroits, Donnee
    db.create_all()
    db.session.commit()

    newuser(idU     = "tanguy",
            nomU    = "voiry",
            mdpU    = "test",
            prenomU = "tanguy")


    newuser(idU     = "florian",
            nomU    = "thomas",
            mdpU    = "test",
            prenomU = "florian")


    newuser(idU     = "maxime",
            nomU    = "deboffle",
            mdpU    = "test",
            prenomU = "maxime")


    newuser(idU     = "pierre",
            nomU    = "lemiere",
            mdpU    = "test",
            prenomU = "pierre")


    newuser(idU     = "joshua",
            nomU    = "vanoz",
            mdpU    = "test",
            prenomU = "joshua")

    bac = Parterre(name = "Bac à sable")

    db.session.add(bac)
    c = Coordonnees(x        = 0,
                    y        = 0,
                    parterre = bac.get_id(),
                    num      = 0)
    bac.add_coordonnee(c)

    typeM1 = TypeMesure(name = "Humidite")
    typeM2 = TypeMesure(name = "Temperature")
    db.session.add(typeM1)
    db.session.add(typeM2)

    p1 = Parterre(name        = "Parterre1")
    c1 = Coordonnees(x        = 6081088.3306859,
                     y        = 214343.058384172,
                     parterre = p1.get_id(),
                     num      = 0)
    p1.add_coordonnee(c1)

    c2 = Coordonnees(x        = 6080868.57422958,
                     y        = 214233.180156012,
                     parterre = p1.get_id(),
                     num      = 1)
    p1.add_coordonnee(c2)

    c3 = Coordonnees(x        = 6080682.25897314,
                     y        = 214596.256040366,
                     parterre = p1.get_id(),
                     num      = 2)
    p1.add_coordonnee(c3)

    c4 = Coordonnees(x        = 6080940.2339436,
                     y        = 214801.680553883,
                     parterre = p1.get_id(),
                     num      = 3)
    p1.add_coordonnee(c4)

    c5 = Coordonnees(x        = 6081088.3306859,
                     y        = 214343.058384172,
                     parterre = p1.get_id(),
                     num      = 4)
    p1.add_coordonnee(c5)

    db.session.add(p1)
    db.session.commit()

    capteur = Capteur(name       = "Capteur1",
                      intervalle = 4,
                      tel        = "0123456789",
                      TypeMesure = typeM1.get_id(),
                      parterre   = p1.get_id())
    db.session.add(capteur)

    capteur2 = Capteur(name       = "Capteur2",
                      intervalle = 4,
                      tel        = "0123456789",
                      TypeMesure = typeM2.get_id(),
                      parterre   = p1.get_id())
    db.session.add(capteur2)

    db.session.commit()

    plante1 = TypePlante(nomPlant = "Magnolia",
                     comportement = "Vivace",
                     taux_humidite = 0.8,
                     quantite = 10,
                     parterre_id = p1.get_id())
    p1.add_plante(plante1)

    plante2 = TypePlante(nomPlant = "Glaïeuls",
                     comportement = "Français",
                     taux_humidite = 0.5,
                     quantite = 15,
                     parterre_id = p1.get_id())
    p1.add_plante(plante2)

    donnee1 = Donnee(value   = 15,
                     date    = datetime.strptime('Jun 18 2018  10:14AM', '%b %d %Y %I:%M%p'),
                     capteur = capteur.get_id(),
                     parterre = p1.get_id())
    db.session.add(donnee1)

    donnee2 = Donnee(value   = 25,
                     date    = datetime.strptime('Jun 18 2018  11:14AM', '%b %d %Y %I:%M%p'),
                     capteur = capteur.get_id(),
                     parterre = p1.get_id())
    db.session.add(donnee2)

    donnee3 = Donnee(value   = 12,
                     date    = datetime.strptime('Jun 18 2018  12:14PM', '%b %d %Y %I:%M%p'),
                     capteur = capteur.get_id(),
                     parterre = p1.get_id())
    db.session.add(donnee3)

    donnee4 = Donnee(value   = 3,
                     date    = datetime.strptime('Jun 18 2018  10:14AM', '%b %d %Y %I:%M%p'),
                     capteur = capteur2.get_id(),
                     parterre = p1.get_id())
    db.session.add(donnee4)

    donnee5 = Donnee(value   = 42,
                     date    = datetime.strptime('Jun 18 2018  11:14AM', '%b %d %Y %I:%M%p'),
                     capteur = capteur2.get_id(),
                     parterre = p1.get_id())
    db.session.add(donnee5)

    donnee6 = Donnee(value   = 36,
                     date    = datetime.strptime('Jun 18 2018  12:14PM', '%b %d %Y %I:%M%p'),
                     capteur = capteur2.get_id(),
                     parterre = p1.get_id())
    db.session.add(donnee6)

    db.session.commit()

    donnee1 = Donnee


@manager.command
def syncdb():
    '''Creates all mising tables'''
    db.create_all()

@manager.command
def newuser(idU,nomU,mdpU,prenomU):
    '''adds a new user.'''
    from .models import Utilisateur
    from hashlib import sha256
    m = sha256()
    m.update(mdpU.encode())
    u=Utilisateur(idU=idU,nomU=nomU,mdpU=m.hexdigest(),prenomU=prenomU)
    db.session.add(u)
    db.session.commit()

@manager.command
def passwd(username,password):
    from .models import User,get_user
    from hashlib import sha256
    m = sha256()
    m.update(password.encode())
    user=get_user(username)
    user.password=m.hexdigest()
    db.session.commit()
