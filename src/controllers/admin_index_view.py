# src/controllers/base_admin_index_view.py
from flask_admin import AdminIndexView, expose
from flask_login import current_user
from flask import redirect, url_for

class BaseAdminIndexView(AdminIndexView):
    def __init__(self, role, *args, **kwargs):
        self.role = role
        super(BaseAdminIndexView, self).__init__(*args, **kwargs)

    @expose('/')
    def index(self):
        if not (current_user.is_authenticated and current_user.role == self.role):
            return redirect(url_for('user_ctrl.login'))
        return super(BaseAdminIndexView, self).index()
