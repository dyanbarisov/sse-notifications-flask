from platforms import models, admin, db
from flask_admin.contrib.sqla import ModelView
from flask_security import current_user
from flask import url_for, redirect, request, abort


class MyModelView(ModelView):
    edit_template = 'my_edit.html'

    def is_accessible(self):
        return (current_user.is_active and
                current_user.is_authenticated and
                current_user.has_role('superuser')
        )

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


# Create admin
admin.add_view(MyModelView(models.User, db.session))
admin.add_view(MyModelView(models.Role, db.session))
