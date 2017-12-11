# Secure views
# ------------
from admin import ModelView
from extensions import db, admin
from .models import Graphique, Colonne

admin.add_view(ModelView(Graphique, db.session, category='Graphique'))
admin.add_view(ModelView(Colonne, db.session, category='Graphique'))
