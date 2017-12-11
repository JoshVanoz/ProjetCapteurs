from flask_security.forms import RegisterForm
from wtforms import StringField
from wtforms.validators import Required
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, HiddenField
from .models import User
from hashlib import sha256

class ExtendedRegisterForm(RegisterForm):
    username = StringField("Nom d'utilisateur");



class LoginForm(FlaskForm):

    email = StringField('Adresse mail')
    password = PasswordField('Mot de passe')
    next = HiddenField()

    def get_authenticated_user(self):
        user = User.query.filter_by(email=self.email.data)
        if user is None:
            return None
        m = sha256()
        m.update(self.password.data.encode())
        passwd = m.hexdigest()
        return user if passwd == user.password else None
