from src.models.car_model import CarTypeEnum
from src.models.service_model import ServiceModel
from src.models.slot_model import SlotModel
from src.models.carwash_model import CarWashModel
from src.models.extra_model import ExtraModel
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, DateTimeField, BooleanField
from wtforms_sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField
from wtforms.validators import DataRequired
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
        else:
            self.carwash.query_factory = lambda: self.session.query(CarWashModel).all()
            self.service.query_factory = lambda: self.session.query(ServiceModel).all()
            
            self.extras.query_factory = lambda: self.session.query(ExtraModel).all()

        self.slot.query_factory = lambda: []
        
    # Form fields
    new_car_license_plate = StringField('Rendszám', validators=[DataRequired()])
    new_car_type = SelectField('Méret', choices=[(t.name, t.name) for t in CarTypeEnum], validators=[DataRequired()])
    new_car_brand = StringField('Márka', validators=[DataRequired()])
    new_car_model = StringField('Típus', validators=[DataRequired()])

    new_customer_forname = StringField('Keresztnév', validators=[DataRequired()])
    new_customer_lastname = StringField('Vezetéknév', validators=[DataRequired()])
    new_customer_phone_number = StringField('Telefonszám', validators=[DataRequired()])

    service = QuerySelectField('Csomag', allow_blank=False, query_factory=lambda: [],validators=[DataRequired()])
    extras = QuerySelectMultipleField('Extrák', get_label='service_name')

    reservation_date = DateTimeField('Időpont', format='%Y-%m-%d %H:%M:%S',validators=[DataRequired()])
    parking_spot = StringField('Parkolóhely')
    carwash = QuerySelectField('Autómosó', allow_blank=False, query_factory=lambda: [])
    slot = QuerySelectField('Slot', allow_blank=False, query_factory=lambda: [])
    is_completed = BooleanField('Kész?')
    
    
    billing_required = BooleanField('Számlát kér')
    billing_name = StringField('Név (számla)')
    address = StringField('Cím')
    email = StringField('E-mail')
    company_name = StringField('Cégnév')
    tax_ID = StringField('Adószám')