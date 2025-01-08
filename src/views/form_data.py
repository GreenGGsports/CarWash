import inspect
from src.models.car_model import CarTypeEnum

class FormData():
    @classmethod
    def parseForm(cls, form_data):
        cls_params = inspect.signature(cls).parameters
        filtered_data = {key: form_data.get(key) for key in cls_params}
        missing_fields = [key for key, param in cls_params.items() if param.default == inspect.Parameter.empty and key not in form_data]
        if missing_fields:
            raise ValueError(f"Missing required fields: {', '.join(missing_fields)}")
        return cls(**filtered_data)
    
class ReservationData(FormData):
    def __init__(
        self,
        reservation_date,
        payment_method,
        parking_spot: str,
        is_completed: bool = False,
        final_price: int = None,
        comment: str = None
    ):
        self.reservation_date = reservation_date
        self.payment_method = payment_method
        self.parking_spot = parking_spot
        self.is_completed = is_completed
        self.final_price = final_price
        self.comment = comment

        self.kwargs = dict(
            reservation_date=self.reservation_date,
            payment_method=self.payment_method,
            parking_spot=self.parking_spot,
            is_completed=self.is_completed,
            final_price=self.final_price,
            comment=self.comment,
        )
    
class BillingData(FormData):
    def __init__(self, billing_name, address, email, company_name, tax_ID):
        self.name = billing_name
        self.address = address
        self.email = email
        self.company_name = company_name
        self.tax_ID = tax_ID
        self.kwargs = dict(
            name=self.name,
            address=self.address,
            email=self.email,
            company_name=self.company_name,
            tax_ID=self.tax_ID
        )

class CarData(FormData):
    def __init__(
        self,
        new_car_license_plate,
        new_car_type,
        new_car_brand,
        new_car_model,
    ):
        self.license_plate = new_car_license_plate
        self.car_type = new_car_type
        self.car_brand = new_car_brand
        self.car_model = new_car_model

        self.kwargs = dict(
            license_plate=self.license_plate,
            car_type=CarTypeEnum[self.car_type],
            car_brand=self.car_brand,
            car_model=self.car_model,
        )