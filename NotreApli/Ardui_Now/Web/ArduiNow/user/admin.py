# Secure views
# ------------
from admin import ModelView
from extensions import db, admin
from .models import User, Role


class UserView(ModelView):
    column_list = ['username', 'email', 'active', 'created']

admin.add_view(UserView(User, db.session, category='Auth'))
admin.add_view(ModelView(Role, db.session, category='Auth'))
