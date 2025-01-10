from flask_login import current_user
from flask import redirect, url_for
from src.views.my_modelview import MyModelView
from src.models.extra_model import ExtraModel
from wtforms_sqlalchemy.fields import QuerySelectMultipleField

class ServiceModelView(MyModelView):
    column_labels = {
        'carwash.carwash_name': 'Car Wash Name',
        'service_name': 'Service Name',
        'price_small': 'Price (Small)',
        'price_medium': 'Price (Medium)',
        'price_large': 'Price (Large)', 
        'extras': 'Tartalom',
    }

    column_list = ['carwash.carwash_name', 'extras',  'service_name', 'price_small', 'price_medium', 'price_large']

    def edit_form(self, obj=None):
        """
        Customize the edit form to limit extras based on the currently edited object.
        """
        # Call the parent method to get the form
        form = super().edit_form(obj)
        
        # Check if the object exists and limit the extras field accordingly
        if obj and obj.carwash_id:
            # Filter extras by the carwash_id of the current object
            form.extras.query_factory = lambda: self.session.query(ExtraModel).filter_by(carwash_id=obj.carwash_id).all()
        elif current_user.role == 'local_admin' and current_user.carwash_id:
            # Limit to extras for the current user's carwash_id
            form.extras.query_factory = lambda: self.session.query(ExtraModel).filter_by(carwash_id=current_user.carwash_id).all()
        else:
            # Fallback: allow all extras
            form.extras.query_factory = lambda: self.session.query(ExtraModel).all()

        return form
    
    def create_form(self, obj=None):
        """
        Customize the create form to remove the extras field for adding new records.
        """
        # Call the parent method to get the form
        form = super().create_form(obj)

        # Remove the 'extras' field from the form
        del form.extras

        return form
    
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
    
    