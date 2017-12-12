from .app import manager, db
@manager.command

def loaddb():
    db.create_all()

    from .models import Capteur, Utilisateur, Parterre, TypePlante, TypeMesure, AlesDroits, Donnee
    
