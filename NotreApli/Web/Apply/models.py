from .app import db,login_manager
from flask_login import UserMixin

class Utilisateur(db.Model):
    idU = db.Column(db.String(50), primary_key=True)
    nomU = db.Column(db.String(20))
    mdpU = db.Column(db.String(100))
    prenomU = db.Column(db.String(20))

    def __repr__(self):
        return "<Utilisateur (%d) %s>" % (self.idU, self.nomU)

class Parterre(db.Model):
    idP = db.Column(db.Integer, primary_key=True)
    nomP = db.Column(db.String(100))
    lieuGeoPX= db.Column(db.Float)
    lieuGeoPY= db.Column(db.Float)
    def __repr__(self):
        return "<Parterre (%d) %s>" % (self.idP, self.nomP)

class TypePlante(db.Model):
    idPlant = db.Column(db.Integer, primary_key=True)
    NomPlant = db.Column(db.String(100))
    def __repr__(self):
        return "<TypePlante (%d) %s>" % (self.NomPlant)

class TypeMesure(db.Model):
    IdTypeM = db.Column(db.Integer, primary_key=True)
    nomTypeM = db.Column(db.String(100))

    def __repr__(self):
        return "<TypeMesure (%d) %s>" % (self.nomTypeM)


class Capteur(db.Model):
    idCapt = db.Column(db.Integer, primary_key=True)
    lieuGeoCaptX = db.Column(db.Float)
    lieuGeoCaptY = db.Column(db.Float)
    lvlBatCapt = db.Column(db.Integer)
    nomCapt = db.Column(db.String(20))
    datePlacement = db.Column(db.DateTime)
    intervalleTemps = db.Column(db.DateTime)
    numTel = db.Column(db.String(10))

    def __repr__(self):
        return "<Capteur (%d) %s>" % (self.idCapt, self.nomCapt)

class AlesDroits(db.Model):

    Lecture = db.Column(db.Boolean)
    Edition = db.Column(db.Boolean)
    Suppression = db.Column(db.Boolean)
    idP = db.Column(db.Integer, db.ForeignKey("parterre.idP"), primary_key = True)
    idU = db.Column(db.String(50), db.ForeignKey("utilisateur.idU"), primary_key = True)


class Donnee(db.Model):
    val = db.Column(db.Float)
    dateRel = db.Column(db.DateTime, primary_key=True)
    idCapt = db.Column(db.Integer, db.ForeignKey("capteur.idCapt"))
    def __repr__(self):
        return "<Donnee (%d) %s>" % (self.idCapt, self.dateRel, self.val)

def get_user(username):
    return Utilisateur.query.filter(Utilisateur.IdU==username).one()

@login_manager.user_loader
def load_user(username):
    return Utilisateur.query.get(username)

def get_id(idU):
    return Utilisateur.query.get(idU)
