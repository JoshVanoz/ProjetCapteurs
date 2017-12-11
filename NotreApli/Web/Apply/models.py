
class Utilisateur(db.Model):
    idU = db.Column(db.Integer, primary_key=True)
    nomU = db.Column(db.String(20))
    mdpU = db.Column(db.String(100))
    prenomU = db.Column(db.String(20))

class Parterre(db.Model):
    idP = db.Column(db.Integer, primary_key=True)
    nomP = db.Column(db.String(100))
    lieuGeoPX= db.Column(db.Float))
    lieuGeoPY= db.Column(db.Float)

class TypePlante(db.Model):
    idPlant = db.Column(db.Integer, primary_key=True)
    NomPlant = db.Column(db.String(100))

class TypeMesure(db.Model):
    IdTypeM = db.Column(db.Integer, primary_key=True)
    nomTypeM = db.Column(db.String(100))
