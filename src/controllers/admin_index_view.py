from flask_admin import AdminIndexView, expose
from flask_login import current_user
from flask import redirect, url_for

class AdminIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        if not (current_user.is_authenticated and current_user.role == 'admin'):
            return redirect(url_for('user_ctrl.login'))
        return super(AdminIndexView, self).index()
