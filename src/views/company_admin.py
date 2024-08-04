from flask_admin import BaseView, expose
from flask import request
from datetime import datetime
from sqlalchemy import func
from sqlalchemy.orm import joinedload
from src.models.company_model import CompanyModel
from src.models.reservation_model import ReservationModel
from src.models.car_model import CarModel
from src.models.service_model import ServiceModel
from src.models.extra_model import ExtraModel

class MonthlyInvoiceView(BaseView):
    def __init__(self, session, *args, **kwargs):
        self.session = session
        super(MonthlyInvoiceView, self).__init__(*args, **kwargs)
    
    @expose('/', methods=['GET', 'POST'])
    def index(self):
        now = datetime.now()
        year = now.year
        month = now.month
        company_name = ''

        if request.method == 'POST':
            year = int(request.form.get('year', year))
            month = int(request.form.get('month', month))
            company_name = request.form.get('company_name', '')

        invoices = self.get_monthly_invoices(self.session, year, month, company_name)
        total_amount = self.get_total_amount(self.session, year, month, company_name)

        companies = self.session.query(CompanyModel.company_name).all()

        return self.render('admin/invoice.html', 
                           invoices=invoices, 
                           total_amount=total_amount,
                           companies=companies, 
                           selected_year=year, 
                           selected_month=month, 
                           selected_company_name=company_name,
                           now=now)
    
    def get_monthly_invoices(self, session, year, month, company_name):
        start_date = datetime(year, month, 1)
        if month == 12:
            end_date = datetime(year + 1, 1, 1)
        else:
            end_date = datetime(year, month + 1, 1)
        
        # Lekérdezés a havi számlák összesítéséhez
        query = session.query(
            CompanyModel.company_name,
            ReservationModel.id,
            func.sum(ReservationModel.final_price).label('total_amount')
        ).select_from(CompanyModel).join(CarModel).join(ReservationModel).filter(
            ReservationModel.reservation_date >= start_date,
            ReservationModel.reservation_date < end_date
        )
        
        if company_name:
            query = query.filter(CompanyModel.company_name.like(f'%{company_name}%'))
        
        invoices = query.group_by(
            CompanyModel.company_name,
            ReservationModel.id
        ).all()
        
        # Lekérdezzük a kapcsolódó adatokat külön lekérdezéssel
        reservation_ids = [invoice[1] for invoice in invoices]
        reservations = session.query(ReservationModel).options(
            joinedload(ReservationModel.customer),
            joinedload(ReservationModel.service),
            joinedload(ReservationModel.extras),
            joinedload(ReservationModel.car)
        ).filter(
            ReservationModel.id.in_(reservation_ids)
        ).all()

        # Készíts egy szótárt az azonosítók alapján
        reservation_dict = {reservation.id: reservation for reservation in reservations}
        
        # Csatlakoztassuk az adatokat
        result = []
        for invoice in invoices:
            reservation = reservation_dict.get(invoice[1])
            result.append({
                'company_name': invoice.company_name,
                'licence_plate':reservation.car.license_plate if reservation.car else None,
                'customer_forename': reservation.customer.forname if reservation.customer else None,
                'customer_lastname': reservation.customer.lastname if reservation.customer else None,
                'service_name': reservation.service.service_name if reservation.service else None,
                'extras': [extra.service_name for extra in reservation.extras] if reservation.extras else [],
                'total_amount': invoice.total_amount
            })
        
        return result
    def get_total_amount(self, session, year, month, company_name):
        start_date = datetime(year, month, 1)
        if month == 12:
            end_date = datetime(year + 1, 1, 1)
        else:
            end_date = datetime(year, month + 1, 1)
        
        query = session.query(
            func.sum(ReservationModel.final_price).label('total_amount')
        ).join(CarModel).join(CompanyModel).filter(
            ReservationModel.reservation_date >= start_date,
            ReservationModel.reservation_date < end_date
        )
        
        if company_name:
            query = query.filter(CompanyModel.company_name.like(f'%{company_name}%'))
        
        total_amount = query.scalar()
        
        return total_amount or 0

    def get_companies(self):
        # Lekérdezzük az összes céget a legördülő menühöz
        return self.session.query(CompanyModel.company_name).distinct().all()
