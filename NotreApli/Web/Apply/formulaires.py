from flask_wtf import FlaskForm
from wtforms import HiddenField, StringField, PasswordField, IntegerField, DateField, FloatField, validators
import datetime
from wtforms.validators import DataRequired
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from .models import *
from hashlib import sha256

class LoginForm(FlaskForm):
    """
    Login formular. Used to connect an user to the application.
    """

    username = StringField("Username")
    password = PasswordField("Password")
    next     = HiddenField()

    def get_id(self):
        return self.username.data

    def get_password(self):
        return self.password.data

    def get_authenticated_user(self):
        user = load_user(self.username.data)
        if user is None:
            return None
        from hashlib import sha256
        m = sha256()
        m.update(self.password.data.encode())
        passwd = m.hexdigest()
        return user if passwd == user.mdpU else None

    def get_next(self):
        return self.next.data

    def set_next(self, newNext):
        self.next.data = newNext

class InscriptionForm(FlaskForm):

    username = StringField("Username")
    password = PasswordField("Password")
    confirm  = PasswordField("Confirm password")
    nom      = StringField("Nom")
    prenom   = StringField("Prénom")

    def get_id(self):
        return self.username.data

    def get_mdp(self):
        return self.password.data

    def get_name(self):
        return self.nom.data

    def get_surname(self):
        return self.prenom.data

    def uniq_Username(self):
        return load_user(self.username.data) == None

    def passwd_confirmed(self):
        return self.password.data == self.confirm.data


class CapteurForm(FlaskForm):
    """
    Creation and Edition Sensor formular. Used to create or to modify a Sensor.
    """

    id           = HiddenField('id')
    name         = StringField('Nom', validators = [DataRequired()])
    intervalTime = IntegerField('Intervalle temps')
    phoneNumber  = StringField('Numéro de téléphone')
    TypeMesure   = QuerySelectField("Type de mesure mesurée :", query_factory = lambda : get_typeMesures())
    parterre     = QuerySelectField("Parterre associé :", query_factory = lambda : get_parterres())
    next         = HiddenField()

    def __init__(self, capteur=None):
        """
        Constructor
        """
        super().__init__()
        if capteur:
            self.id.data           = capteur.get_id()
            self.name.data         = capteur.get_name()
            self.phoneNumber.data  = capteur.get_phoneNumber()
            self.TypeMesure.data   = get_typeMesure(capteur.get_typeMesure())
            self.parterre.data     = get_parterre(capteur.get_parterre())
            self.intervalTime.data = capteur.get_interval()
            self.next.data         = "save_capteur"
        else:
            self.next.data = "new_capteur_saving"

    def get_id(self):
        return self.id.data

    def get_interval(self):
        return self.intervalTime.data

    def get_name(self):
        return self.name.data

    def get_parterre(self):
        return self.parterre.data

    def get_phoneNumber(self):
        return self.phoneNumber.data

    def get_typeMesure(self):
        return self.TypeMesure.data

    def get_next(self):
        return self.next.data


class ParterreForm(FlaskForm):

    id        = HiddenField('id')
    nomP      = StringField('Nom', validators = [DataRequired()])
    lieuGeoPX = FloatField('Position X')
    lieuGeoPY = FloatField('Position Y')
    next      = HiddenField()

    def __init__(self, parterre=None):
        super().__init__()
        if parterre:
            self.id.data        = parterre.get_id()
            self.nomP.data      = parterre.get_name()
            self.lieuGeoPX.data = parterre.get_coordonnees()[0]
            self.lieuGeoPY.data = parterre.get_coordonnees()[1]
            self.next.data      = "save_parterre"
        else:
            self.next.data      = "new_parterre_saving"

    def get_id(self):
        return self.id.data

    def get_name(self):
        return self.nomP.data

    def get_coordonnees(self):
        return (self.lieuGeoPX.data, self.lieuGeoPY.data)

    def get_next(self):
        return self.next.data

class PlanteForm(FlaskForm):

    id = HiddenField('id')
    nom_plante = StringField('Nom', validators = [DataRequired()])
    comportement = StringField('comportement')
    taux_humidite = FloatField('Taux en humidité nécessaire')
    quantite = IntegerField('Nombre')
    parterre = QuerySelectField("Parterre associé :", query_factory = lambda : get_parterres())
    next = HiddenField()

    def __init__(self, plante=None):
        super().__init__()
        if plante :
            self.id.data = plante.get_id()
            self.nom_plante.data = plante.get_name()
            self.comportement.data = plante.get_comportement()
            self.taux_humidite.data = plante.get_taux_humidite()
            self.quantite.data = plante.get_quantite()
            self.parterre.data = get_parterre(capteur.get_parterre())
            self.next.data = "save_plante"
        else:
            self.next.data = "new_plante_saving"

    def get_name(self):
        return self.nom_plante.data

    def get_id(self):
        return self.id.data

    def get_comportement(self):
        return self.comportement.data

    def get_taux_humidite(self):
        return self.taux_humidite.data

    def get_quantite(self):
        return self.quantite.data

    def get_parterre(self):
        return self.parterre.data

    def get_next(self):
        return self.next.data
