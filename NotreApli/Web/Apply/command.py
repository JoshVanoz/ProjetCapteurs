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
def passwd(idU,password):
    '''modifier password user'''
    from .models import Utilisateur
    
