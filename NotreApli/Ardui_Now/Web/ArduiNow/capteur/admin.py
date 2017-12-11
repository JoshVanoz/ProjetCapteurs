# Secure views
# ------------
from admin import ModelView
from extensions import db, admin
from .models import Capteur, Mesure, Geolocalisation

admin.add_view(ModelView(Capteur, db.session, category='Capteurs'))
admin.add_view(ModelView(Mesure, db.session, category='Capteurs'))
admin.add_view(ModelView(Geolocalisation, db.session, category='Capteurs'))
