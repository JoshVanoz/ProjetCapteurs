from flask_wtf import FlaskForm
from wtforms import HiddenField, StringField, PasswordField, IntegerField, DateField, FloatField, validators
import datetime
from wtforms.validators import DataRequired
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from .models import *
from hashlib import sha256
from flask_login import login_user,current_user, logout_user, login_required

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


class CapteurForm(FlaskForm):
    """
    Creation and Edition Sensor formular. Used to create or to modify a Sensor.
    """

    id   = HiddenField('id')
    name = StringField('Nom', validators = [DataRequired()])
    lieuGeoX = FloatField('Position X')
    lieuGeoY = FloatField('Position Y')
    lvlBattery = IntegerField('Level de la Batterie')
    placementDate = DateField('Date de placement', format='%m/%d/%Y', validators=(validators.Optional(),))
    intervalTime = IntegerField('Intervalle temps')
    phoneNumber = StringField('Numéro de téléphone')
    TypeMesure = QuerySelectField("Type de mesure mesurée :", query_factory = lambda : get_TypeMesures())
    parterre = QuerySelectField("Parterre associé :", query_factory = lambda : get_parterres())
    next = HiddenField()

    def __init__(self, id=None, name=None, phone="0000000000", mesure=None, parterre=None):
        """
        Constructor
        """
        super().__init__()
        if id:
            self.id.data = id
            self.name.data = name
            self.phoneNumber = phone
            self.TypeMesure = mesure
            self.parterre = parterre
            self.lieuGeoX = 0
            self.lieuGeoY = 0
            self.lvlBattery = 100
            self.placementDate = datetime.datetime.now()
            self.intervalTime = 5
            self.next.data = "save_capteur"
        else:
            self.next.data = "new_capteur_saving"

    def get_id(self):
        return self.id.data

    def get_name(self):
        return self.name.data

    def get_next(self):
        return self.next.data

    def set_name(self, newName):
        self.album_name.data = newName

    def get_lvlBattery(self):
        return self.lvlBattery

    def set_lvlBattery(self, newValue):
        self.lvlBattery = newValue

    def get_placementDate(self):
        return self.placementDate

    def get_phoneNumber(self):
        return self.phoneNumber

    def set_phoneNumber(self, newValue):
        self.phoneNumber = newValue

    def get_TypeMesure(self):
        return self.TypeMesure

    def get_Parterre(self):
        return self.parterre
