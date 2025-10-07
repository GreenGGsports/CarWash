from src.models.car_model import CarTypeEnum
from src.models.reservation_model import PaymentEnum
from src.models.service_model import ServiceModel
from src.models.slot_model import SlotModel
from src.models.carwash_model import CarWashModel
from src.models.extra_model import ExtraModel
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, DateTimeField, BooleanField, FloatField
from wtforms_sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField
from wtforms.validators import DataRequired,  Optional
from flask_login import current_user
from src.models.company_model import CompanyModel

class ReservationForm(FlaskForm):
    def __init__(self, session, obj=None, *args, **kwargs):
        super(ReservationForm, self).__init__(*args, **kwargs)
        self.session = session

        allowed_carwashes = [cw.id for cw in current_user.carwash] if current_user.carwash else []

        self.carwash.query_factory = lambda: self.session.query(CarWashModel).filter(CarWashModel.id.in_(allowed_carwashes)).all()
        self.service.query_factory = lambda: self.session.query(ServiceModel).filter(ServiceModel.carwash_id.in_(allowed_carwashes)).all()
        
        self.extras.query_factory = lambda: self.session.query(ExtraModel).all()
        allowed_ids = [c.id for c in current_user.companies]


        self.new_car_company.query_factory = lambda: self.session.query(CompanyModel).filter(CompanyModel.id.in_(allowed_ids)).all()
        self.slot.query_factory = lambda: self.session.query(SlotModel).filter_by(live=True).all()

    def load_data(self, obj):
        """Betölti az adatokat a foglalás objektumból az űrlap mezőibe."""
        if obj.car:
            self.new_car_license_plate.data = obj.car.license_plate
            self.new_car_type.data = obj.car.car_type.name  # Enum név
            self.new_car_brand.data = obj.car.car_brand
            self.new_car_model.data = obj.car.car_model
            self.new_car_company = obj.car.company

        if obj.customer:
            self.new_customer_forname.data = obj.customer.forname
            self.new_customer_lastname.data = obj.customer.lastname
            self.new_customer_phone_number.data = obj.customer.phone_number

        self.parking_spot.data = obj.parking_spot
        self.reservation_date.data = obj.reservation_date
        self.payment_method.data = obj.payment_method.name if obj.payment_method else None
        self.comment.data = obj.comment if obj.comment else None

        self.carwash.data = obj.carwash
        self.slot.data = obj.slot
        self.service.data = obj.service  # A service objektumot állítjuk be
        self.extras.data = obj.extras  # Az extras listát állítjuk be
        
    # Form fields
    carwash = QuerySelectField('Autómosó', allow_blank=False, query_factory=lambda: [])
    reservation_date = DateTimeField('Időpont', format='%Y-%m-%d',validators=[DataRequired()])
    slot = QuerySelectField('Slot', allow_blank=False, query_factory=lambda: [])
    service = QuerySelectField('Csomag', allow_blank=False, query_factory=lambda: [],validators=[DataRequired()])
    extras = QuerySelectMultipleField('Extrák', get_label='service_name')

    new_car_license_plate = StringField('Rendszám', validators=[DataRequired()])
    new_car_type = SelectField('Méret', choices=[(t.name, t.name) for t in CarTypeEnum], validators=[DataRequired()])
    new_car_brand = StringField('Márka', validators=[DataRequired()])
    new_car_model = StringField('Típus', validators=[DataRequired()])
    new_car_company = QuerySelectField('Cég', allow_blank=False, query_factory=lambda: [],validators=[DataRequired()])

    new_customer_forname = StringField('Keresztnév', validators=[DataRequired()])
    new_customer_lastname = StringField('Vezetéknév', validators=[DataRequired()])
    new_customer_phone_number = StringField('Telefonszám', validators=[DataRequired()])

    comment = StringField('Megjegyzés',validators=[DataRequired()])

    payment_method = SelectField(
    'Fizetési mód',
    choices=[(t.name, t.value) for t in PaymentEnum],
    default=PaymentEnum.list.name,   # 👈 use .name here, not .value
    validators=[DataRequired()]
)

    parking_spot = StringField('Parkolóhely')
    


