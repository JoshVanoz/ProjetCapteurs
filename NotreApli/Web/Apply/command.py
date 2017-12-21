
from .app import manager, db

@manager.command
def loaddb():
    from .models import Capteur, Utilisateur, Parterre, TypePlante, TypeMesure, AlesDroits, Donnee
    db.create_all()
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
