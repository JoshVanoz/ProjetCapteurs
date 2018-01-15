from flask_wtf import FlaskForm
from wtforms import HiddenField, StringField, PasswordField, IntegerField, DateField, FloatField, validators
import datetime
from wtforms.validators import DataRequired
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from .models import get_TypeMesures, get_parterres

class UserForm(FlaskForm):
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

    def get_authentificated_user(self):
        user = load_user(self.username.data)
        if user is None:
            return None
        from hashlib import sha256
        m = sha256()
        m.update(self.password.data.encode())
        passwd = m.hexdigest()
        return user if passwd == user.get_password() else None

    def get_next(self):
        return self.next.data

    def set_next(self, newNext):
        self.next.data = newNext


class CapteurForm(FlaskForm):
    """
    Creation and Edition Sensor formular. Used to create or to modify a Sensor.
    """

    id   = HiddenField('id')
    name = StringField('Nom', validators = [DataRequired()])
    lieuGeoX = FloatField('Position X')
    lieuGeoY = FloatField('Position Y')
    lvlBattery = IntegerField('Level de la Batterie')
    intervalTime = IntegerField('Intervalle temps')
    phoneNumber = StringField('Numéro de téléphone')
    TypeMesure = QuerySelectField("Type de mesure mesurée :", query_factory = lambda : get_TypeMesures())
    parterre = QuerySelectField("Parterre associé :", query_factory = lambda : get_parterres())
    next = HiddenField()

    def __init__(self, capteur=None):
        """
        Constructor
        """
        super().__init__()
        if capteur:
            self.id.data = capteur.get_id()
            self.name.data = capteur.get_name()
            self.phoneNumber.data = capteur.get_phoneNumber()
            self.TypeMesure.data = capteur.get_TypeMesure()
            self.parterre.data = capteur.get_parterre()
            self.lieuGeoX.data = capteur.get_coordonnees()[0]
            self.lieuGeoY.data = capteur.get_coordonnees()[1]
            self.lvlBattery.data = capteur.get_lvlBattery()
            self.intervalTime.data = capteur.get_interval()
            self.next.data = "new_capteur_saving"
        else:
            self.next.data = "new_capteur_saving"

    def get_id(self):
        return self.id.data

    def get_interval(self):
        return self.intervalTime.data

    def get_name(self):
        return self.name.data

    def get_Parterre(self):
        return self.parterre.data

    def get_next(self):
        return self.next.data

    def set_name(self, newName):
        self.album_name.data = newName

    def get_lvlBattery(self):
        return self.lvlBattery.data

    def set_lvlBattery(self, newValue):
        self.lvlBattery = newValue

    def get_phoneNumber(self):
        return self.phoneNumber.data

    def set_phoneNumber(self, newValue):
        self.phoneNumber = newValue

    def get_TypeMesure(self):
        return self.TypeMesure.data

    def get_parterre(self):
        return self.parterre.data

    def get_coordonnees(self):
        return (self.lieuGeoX.data,self.lieuGeoY.data)
