from .app import db

class Capteur(db.Model):
    idCapt = db.Column(db.Integer, primary_key=True)
    lieuGeoCaptX = db.Column(db.Float)
    lieuGeoCaptY = db.Column(db.Float)
    lvlBatCapt = db.Column(db.Integer))
    nomCapt = db.Column(db.String(20))
    datePlacement = db.Column(db.DateTime.Date)
    intervalleTemps = db.Column(db.DateTime.time)
    numTel = db.Column(db.String(10))

class AlesDroits(db.Model):
    Lecture = db.Column(db.Boolean)
    Edition = db.Column(db.Boolean)
    Suppression = db.Column(db.Boolean)
