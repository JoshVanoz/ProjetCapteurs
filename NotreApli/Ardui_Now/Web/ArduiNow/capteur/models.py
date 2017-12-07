import datetime
import json

from extensions import db
import datetime


# capteur de type arduino
class Capteur(db.Model):

    captId = db.Column(db.Integer, primary_key=True)
    cName = db.Column(db.String(100))
    cTel = db.Column(db.String(20))
    cType = db.Column(db.String(100))
    frequence = db.Column(db.Float(5,2))
    formule=db.Column(db.String(255))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), index=True)
    owner = db.relationship('User', backref=db.backref('capteurs', lazy='dynamic'))

    # méthode d'affichage
    def __repr__(self):
        return "<Capteur (%d) %s>" % (self.captId, self.cName)

    @property
    def position(self):
        return self.positions.first()

    def serialize(self):
        return {
            'captId': self.captId,
            'cName': self.cName,
            'cTel': self.cTel,
            'cType': self.cType,
            'frequence': self.frequence,
            'formule': self.frequence,
            'pos_x': self.position.position_x,
            'pos_y': self.position.position_y,
        }


# géolocalisation d'un capteur
class Geolocalisation(db.Model):

    position_x = db.Column(db.Float)
    position_y = db.Column(db.Float)
    capt_id = db.Column(db.Integer, db.ForeignKey('capteur.captId'), primary_key=True)
    capteur = db.relationship('Capteur', backref=db.backref('positions', lazy='dynamic'))
    date = db.Column(db.DateTime, primary_key=True, index=True, server_default=db.func.now(), default=datetime.datetime.utcnow)


# mesure relevée par un capteur
class Mesure(db.Model):

    capt_id = db.Column(db.Integer, db.ForeignKey('capteur.captId'), primary_key=True)
    capteur = db.relationship('Capteur', backref=db.backref('mesures', lazy='dynamic'))
    date = db.Column(db.DateTime, index=True, primary_key=True, server_default=db.func.now(), default=datetime.datetime.utcnow)
    valeur = db.Column(db.Float)


    ## METHODES ##

# on récupère un capteur par son id
def get_capteur(id):
    return Capteur.query.get(id)

# on récupère un capteur par son nom
def get_capteur_by_name(name):
    return Capteur.query.filter_by(cName=name)

# on récupère la position d'un capteur
def get_position(id):
    return Geolocalisation.query.filter_by(captId=id)

# on récupère la liste des capteurs d'un user
def get_capteurs(user):
    return Capteur.query.filter_by(Capteur.owner==user)
