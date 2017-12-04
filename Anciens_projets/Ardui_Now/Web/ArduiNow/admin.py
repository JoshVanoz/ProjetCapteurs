from flask import request, abort, url_for, redirect
from flask_security import current_user
from flask_admin import (BaseView as _BaseView,
                         AdminIndexView as _AdminIndexView,
                         expose, AdminIndexView)
from flask_admin.contrib.sqla import ModelView as _ModelView

class AuthMixin(object):

    def is_accessible(self):
        if not current_user.is_active or not current_user.is_authenticated:
            return False

        if current_user.has_role('admin'):
            return True

        return False

    def _handle_view(self, name, **kwargs):
        """
        Override builtin _handle_view in order to redirect users when a view is not accessible.
        """
        if not self.is_accessible():
            if current_user.is_authenticated:
                # permission denied
                abort(403)
            else:
                # login
                return redirect(url_for('security.login', next=request.url))


class AdminIndex(AuthMixin, AdminIndexView):
    # use a custom template for the admin home page
    @expose('/')
    def index(self):
        return self.render(self._template)


class BaseView(AuthMixin, _BaseView):
    pass


class ModelView(AuthMixin, _ModelView):
    pass