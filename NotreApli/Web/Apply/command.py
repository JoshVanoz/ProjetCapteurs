from .app import manager, db

@manager.command
def loaddb():
    from .models import Capteur, Utilisateur, Parterre, TypePlante, TypeMesure, AlesDroits, Donnee
    db.create_all()
    db.session.commit()
