# src/views/base_modelview.py
from flask_admin.contrib.sqla import ModelView
from flask import flash, current_app
from flask_login import current_user
from flask import redirect, url_for, request


class MyModelView(ModelView):
    def __init__(self, *args, **kwargs):
        self.role = kwargs.pop('role', None)
        super(MyModelView, self).__init__(*args, **kwargs)
    
    def is_accessible(self):
        # Check if the user is authenticated and has the required role
        if not current_user.is_authenticated:
            return False
        if self.role and current_user.role != self.role:
            return False
        return True

    def inaccessible_callback(self, name, **kwargs):
        # Redirect to login if access is denied
        return redirect(url_for('user_ctrl.login'))
    
    def on_model_change(self, form, model, is_created):
        try:
            self.session.add(model)
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            current_app.logger.error(e)
        super(MyModelView, self).on_model_change(form, model, is_created)

    def handle_view_exception(self, exc):
        flash(f'An unexpected error occurred: {exc}', 'error')
        return False

