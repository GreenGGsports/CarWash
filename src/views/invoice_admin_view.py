from flask_login import current_user
from flask import redirect, url_for
from src.views.my_modelview import MyModelView
from src.models.billing_model import BillingModel
from src.views.filters import ThisMonthFilter, ThisWeekFilter, TodayFilter
from flask_admin.contrib.sqla.filters import DateBetweenFilter,  FilterLike
class InvoiceModelView(MyModelView):
    can_create = False
    can_delete = False
    can_edit = True
    column_labels = {
        'reservation.reservation_date': 'Dátum',
        'reservation.car.license_plate': 'Rendszám',
        'name': 'Név',
        'address': 'Cím',
        'tax_ID': 'Adószám',
        'company_name': 'Cégnév',
        'reservation.payment_method': 'Fizetési mód',
        'reservation.final_price': 'Összeg,'
    }

    column_list = ['reservation.reservation_date','reservation.car.license_plate', 'name', 'address', 'email','company_name', 'tax_ID','reservation.payment_method' ,'reservation.final_price']
    

    column_filters = [
        DateBetweenFilter(BillingModel.reservation.property.mapper.class_.reservation_date, 'Custom date'),
        'reservation.car.license_plate',
        'company_name',
        'reservation.payment_method'
    ]
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
        return super(InvoiceModelView, self)._handle_view(name, **kwargs)
    
    def get_query(self):
        # Alapértelmezett szűrő beállítása az aktuális carwash-ra
        query = super(InvoiceModelView, self).get_query()
        if current_user.role == 'local_admin' and current_user.carwash_id:
            query = query.filter_by(carwash_id=current_user.carwash_id)
        return query