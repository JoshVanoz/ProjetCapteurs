# -*- coding: utf-8 -*-

from flask import Flask, render_template, url_for

from jsonencoder import CustomJSONEncoder
from settings import ProdConfig
from flask_security import Security, SQLAlchemyUserDatastore
from user.forms import ExtendedRegisterForm
from extensions import cache, db, mail, debug_toolbar, migrate, admin
from user.models import User, Role

from public.views import bp_public
from user.views import bp_user
from capteur.views import bp_capteur
from graphique.views import bp_graphique
from jeudedonnees import insert_data


class ArduiNow(Flask):
    def __init__(self, config_object=ProdConfig):
        super().__init__(__name__)
        self.config.from_object(config_object)
        self.register_extensions()
        self.register_blueprints()
        self.register_errorhandlers()
        self.register_shellcontext()
        self.register_commands()

        self.json_encoder = CustomJSONEncoder

    def register_extensions(self):
        cache.init_app(self)
        db.init_app(self)
        user_datastore = SQLAlchemyUserDatastore(db, User, Role)
        security = Security(self, user_datastore, register_form=ExtendedRegisterForm)
        mail.init_app(self)
        debug_toolbar.init_app(self)
        migrate.init_app(self, db)
        admin.init_app(self)

        @security.context_processor
        def security_context_processor():
            return dict(
                admin_base_template=admin.base_template,
                admin_view=admin.index_view,
                # h=admin_helpers,
                get_url=url_for
            )

    def register_blueprints(self):
        self.register_blueprint(bp_public)
        self.register_blueprint(bp_user)
        self.register_blueprint(bp_capteur)
        self.register_blueprint(bp_graphique)

    def register_errorhandlers(self):
        def render_error(error):
            error_code = getattr(error, 'code', 500)
            return render_template("{0}.html".format(error_code)), error_code

        for errcode in [401, 404, 500]:
            self.errorhandler(errcode)(render_error)

    def register_shellcontext(self):
        """Register shell context objects."""

        def shell_context():
            """Shell context objects."""
            return {
                'db': db,
                'User': User}

        self.shell_context_processor(shell_context)

    def register_commands(self):
        """Register Click commands."""
        from commands import clean, create_db, install, reset
        self.cli.add_command(clean)
        self.cli.add_command(create_db)
        self.cli.add_command(install)
        self.cli.add_command(reset)
        self.cli.add_command(insert_data)
