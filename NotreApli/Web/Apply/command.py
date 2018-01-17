
from .app import manager, db

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

    db.session.commit()


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
