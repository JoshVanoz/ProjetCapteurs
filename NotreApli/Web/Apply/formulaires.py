from flask_wtf import FlaskForm
from wtforms import HiddenField, StringField, PasswordField


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
