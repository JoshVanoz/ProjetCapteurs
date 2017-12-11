from extensions import db


class Graphique(db.Model):
    graphId = db.Column(db.Integer, primary_key=True)
    uId = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship("User", backref=db.backref("graphiques", lazy="dynamic"))
    titre = db.Column(db.String(255))

    def __repr__(self):
        return "<Graphique (%d) (%d) (%s) >" % (self.graphId, self.uId, self.titre)


agregats = {
    'max': max,
    'min': min,
    'maximum': max,
    'minimum': min,
    'somme': sum,
    'sum': sum,
    'avg': lambda l: sum(l)/len(l),
    'average': lambda l: sum(l)/len(l),
    'moy': lambda l: sum(l)/len(l),
    'moyenne': lambda l: sum(l)/len(l),
}

agregats_name = {
    'max': "Maximum",
    'min': "Minimum",
    'maximum': "Maximum",
    'minimum': "Minimum",
    'somme': "Somme",
    'sum': "Somme",
    'avg': "Moyenne",
    'average': "Moyenne",
    'moy': "Moyenne",
    'moyenne': "Moyenne",
}


class Colonne(db.Model):
    numCol = db.Column(db.Integer, primary_key=True)
    graphId = db.Column(db.Integer, db.ForeignKey('graphique.graphId'))
    graphique = db.relationship("Graphique", backref=db.backref("colonnes", lazy="dynamic"))
    colName = db.Column(db.String(255))
    dateDebut = db.Column(db.Date())
    dateFin = db.Column(db.Date())
    agregatSimple = db.Column(db.String(255))
    capteur_id = db.Column(db.Integer, db.ForeignKey('capteur.captId'))
    capteur = db.relationship("Capteur")

    def __repr__(self):
        return "<Colonne (%d) (%s) >" % (self.numCol, self.colName)

    @property
    def aggreger(self):
        return agregats.get(self.agregatSimple, lambda x: 0)

    @property
    def valeurs(self):
        valeurs = [m.valeur for m in self.capteur.mesures.all()]
        if not self.agregatSimple:
            return valeurs
        else:
            v = self.aggreger(valeurs)
            return [v for _ in range(len(self.capteur.mesures.all()))]

    @property
    def valeurs_datees(self):
        return list(zip(self.dates, self.valeurs))

    @property
    def dates(self):
        return [m.date for m in self.capteur.mesures.all()]
