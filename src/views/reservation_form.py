from src.models.car_model import CarTypeEnum
from src.models.service_model import ServiceModel
from src.models.slot_model import SlotModel
from src.models.carwash_model import CarWashModel
from src.models.extra_model import ExtraModel
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, DateTimeField, BooleanField
from wtforms_sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField
from flask_login import current_user

class ReservationForm(FlaskForm):
    def __init__(self, session, *args, **kwargs):
        super(ReservationForm, self).__init__(*args, **kwargs)
        self.session = session


        # Filtering options based on the current user
        if current_user.role == 'local_admin':
            self.carwash.query_factory = lambda: self.session.query(CarWashModel).filter_by(id=current_user.carwash.id).all()
            self.service.query_factory = lambda: self.session.query(ServiceModel).filter_by(carwash_id=current_user.carwash.id).all()
            self.extras.query_factory = lambda: self.session.query(ExtraModel).filter_by(carwash_id=current_user.carwash.id).all()
            self.slot.query_factory = lambda: self.session.query(SlotModel).filter_by(carwash_id=current_user.carwash.id, live=True).all()
        else:
            self.carwash.query_factory = lambda: self.session.query(CarWashModel).all()
            self.service.query_factory = lambda: self.session.query(ServiceModel).all()
            
            self.extras.query_factory = lambda: self.session.query(ExtraModel).all()

            self.slot.query_factory = lambda: self.session.query(SlotModel).filter_by(live=True).all()
        
    # Form fields
    new_car_license_plate = StringField('Rendszám')
    new_car_type = SelectField('Méret', choices=[(t.name, t.name) for t in CarTypeEnum])
    new_car_brand = StringField('Márka')

    new_customer_forname = StringField('Keresztnév')
    new_customer_lastname = StringField('Vezetéknév')
    new_customer_phone_number = StringField('Telefonszám')

    service = QuerySelectField('Csomag', allow_blank=False, query_factory=lambda: [])
    extras = QuerySelectMultipleField('Extrák', get_label='service_name')

    reservation_date = DateTimeField('Időpont', format='%Y-%m-%d %H:%M:%S')
    parking_spot = StringField('Parkolóhely')
    carwash = QuerySelectField('Autómosó', allow_blank=False, query_factory=lambda: [])
    slot = QuerySelectField('Slot', allow_blank=False, query_factory=lambda: [])
    is_completed = BooleanField('Kész?')