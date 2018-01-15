from .app import db,login_manager
from flask_login import UserMixin
import datetime

class Utilisateur(db.Model):
    idU = db.Column(db.String(50), primary_key=True)
    nomU = db.Column(db.String(20))
    mdpU = db.Column(db.String(100))
    prenomU = db.Column(db.String(20))

    def __repr__(self):
        return "<Utilisateur (%d) %s>" % (self.idU, self.nomU)

    def get_name(self):
        return self.nomU

    def get_id(self):
        return self.idU

    def set_name(self,nomU):
        self.nomU = nomU

    def set_firstname(self,prenomU):
        self.prenomU = prenomU

    def set_mdp(self,mdpU):
        self.mdpU = mdpU

association_parterre_typePlante = db.Table("association_parterre_typePlante",
                                           db.metadata,
                                           db.Column("parterre_id", db.Integer, db.ForeignKey("parterre.idP"), primary_key = True),
                                           db.Column("type_plante_id", db.Integer, db.ForeignKey("type_plante.idPlant"), primary_key = True))

association_parterre_capteur = db.Table("association_parterre_capteur",
                                        db.metadata,
                                        db.Column("parterre_id", db.Integer, db.ForeignKey("parterre.idP"), primary_key = True),
                                        db.Column("capteur_id", db.Integer, db.ForeignKey("capteur.idCapt"), primary_key = True))
class Parterre(db.Model):
    idP = db.Column(db.Integer, primary_key=True)
    nomP = db.Column(db.String(100))
    lieuGeoPX = db.Column(db.Float)
    lieuGeoPY = db.Column(db.Float)
    plantes = db.relationship("TypePlante",
                              secondary = association_parterre_typePlante,
                              lazy = "dynamic",
                              backref = db.backref("TypePlante", lazy = True))
    capteurs = db.relationship("Capteur",
                               secondary = association_parterre_capteur,
                               lazy = "dynamic",
                               backref = db.backref("Capteur", lazy = True))

    def __repr__(self):
        return "<Parterre (%d) %s>" % (self.idP, self.nomP)

    def get_name(self):
        return self.nomP

    def get_id(self):
        return self.idP

    def set_name(self,nomP):
        self.nomP = nomP

    def set_lieuGeoPX(self,lieuGeoPX):
        self.lieuGeoPX = lieuGeoPX

    def set_lieuGeoPY(self,lieuGeoPY):
        self.lieuGeoPY = lieuGeoPY

    def get_capteurs(self):
        return self.capteurs

    def get_plantes(self):
        return self.plantes

    def add_capteur(self, capteur):
        self.capteurs.append(capteur)

class TypePlante(db.Model):
    idPlant = db.Column(db.Integer, primary_key=True)
    NomPlant = db.Column(db.String(100))
    def __repr__(self):
        return "<TypePlante (%d) %s>" % (self.NomPlant)

    def get_name(self):
        return self.NomPlant

    def get_id(self):
        return self.idPlant

    def set_name(self,NomPlant):
        self.NomPlant = NomPlant


class TypeMesure(db.Model):
    IdTypeM = db.Column(db.Integer, primary_key=True)
    nomTypeM = db.Column(db.String(100))

    def __repr__(self):
        return "<TypeMesure (%d) %s>" % (self.IdTypeM, self.nomTypeM)

    def get_name(self):
        return self.nomTypeM

    def get_id(self):
        return self.IdTypeM

    def set_name(self,nomTypeM):
        self.nomTypeM = nomTypeM

    def get_TypeMesures():
        return TypeMesure.query.order_by(TypeMesure.nomTypeM)


class Capteur(db.Model):
    idCapt = db.Column(db.Integer, primary_key=True)
    lieuGeoCaptX = db.Column(db.Float)
    lieuGeoCaptY = db.Column(db.Float)
    lvlBatCapt = db.Column(db.Integer)
    nomCapt = db.Column(db.String(20))
    datePlacement = db.Column(db.DateTime)
    intervalleTemps = db.Column(db.Integer)
    numTel = db.Column(db.String(10))

    def __init__(self, name, TypeMesure, tel, parterre, x, y, intervalle):
        self.nomCapt = name
        self.lieuGeoCaptX = x
        self.lieuGeoCaptY = y
        self.lvlBatCapt = 50
        self.numTel = tel
        self.datePlacement = datetime.datetime.now()
        self.intervalleTemps = intervalle
        # self.TypeMesure = TypeMesure
        parterre.add_capteur(self)

    def __repr__(self):
        return "<Capteur (%d) %s>" % (self.idCapt, self.nomCapt)

    def get_name(self):
        return self.nomCapt

    def get_id(self):
        return self.idCapt

    def get_coordonnees(self):
        return (self.lieuGeoCaptX, self.set_lieuGeoCaptY)

    def get_date(self):
        return self.datePlacement

    def get_lvlBattery(self):
        return self.lvlBatCapt

    def get_interval(self):
        return self.intervalleTemps

    def get_TypeMesure(self):
        return None

    def get_phoneNumber(self):
        return self.numTel

    def get_parterre(self):
        return None

    def set_name(self,nomCapt):
        self.nomCapt = nomCapt

    def set_lieuGeoCaptX(self,lieuGeoCaptX):
        self.lieuGeoCaptX = lieuGeoCaptX

    def set_lieuGeoCaptY(self,lieuGeoCaptY):
        self.lieuGeoCaptY = lieuGeoCaptY

    def set_num(self,numTel):
        self.numTel = numTel

    def set_interval(self, newInterval):
        self.intervalleTemps = newInterval

class AlesDroits(db.Model):

    Lecture = db.Column(db.Boolean)
    Edition = db.Column(db.Boolean)
    Suppression = db.Column(db.Boolean)
    idP = db.Column(db.Integer, db.ForeignKey("parterre.idP"), primary_key = True)
    idU = db.Column(db.String(50), db.ForeignKey("utilisateur.idU"), primary_key = True)

    def get_id(self):
        return (self.idP, self.idU)

class Donnee(db.Model):
    val = db.Column(db.Float)
    dateRel = db.Column(db.DateTime, primary_key=True)
    idCapt = db.Column(db.Integer, db.ForeignKey("capteur.idCapt"))

    def __repr__(self):
        return "<Donnee (%d) %s>" % (self.idCapt, self.dateRel, self.val)

    def get_id(self):
        return (self.dateRel, self.idCapt)

def get_user(username):
    return Utilisateur.query.filter(Utilisateur.IdU==username).one()

@login_manager.user_loader
def load_user(username):
    return Utilisateur.query.get(username)

def get_id(idU):
    return Utilisateur.query.get(idU)

def get_parterres():
    return Parterre.query.all()

def get_parterre(id):
    return Parterre.query.get(id)

def get_capteurs():
    return Capteur.query.all()

def get_capteur_id(id):
    return Capteur.query.get(id)

def get_TypeMesures():
    return TypeMesure.query.all()
