from flask_login import current_user
from flask import redirect, url_for
from src.views.my_modelview import MyModelView

class ServiceModelView(MyModelView):
    column_labels = {
        'carwash.carwash_name': 'Car Wash Name',
        'service_name': 'Service Name',
        'price_small': 'Price (Small)',
        'price_large': 'Price (Large)'
    }

    column_list = ['carwash.carwash_name', 'service_name', 'price_small', 'price_large']

    def is_accessible(self):
        # Ellenőrizzük, hogy a felhasználó be van-e jelentkezve és admin szerepe van-e
        if current_user.is_authenticated:
            if current_user.role == 'local_admin':
                # Local admin számára csak olvasási jogosultság, az összes módosítási lehetőséget eltávolítjuk
                self.can_create = False
                self.can_edit = False
                self.can_delete = False
                return True
            elif current_user.role == 'admin':
                return True
        return False

    def _handle_view(self, name, **kwargs):
        if not self.is_accessible():
            return redirect(url_for('user_ctrl.login'))
        return super(ServiceModelView, self)._handle_view(name, **kwargs)
    
    def get_query(self):
        # Alapértelmezett szűrő beállítása az aktuális carwash-ra
        query = super(ServiceModelView, self).get_query()
        if current_user.role == 'local_admin' and current_user.carwash_id:
            query = query.filter_by(carwash_id=current_user.carwash_id)
        return query