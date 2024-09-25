from src.models.reservation_model import ReservationModel
from src.models.car_model import CarTypeEnum
from src.views.my_modelview import MyModelView
from flask_login import current_user
from flask import current_app
from src.views.filters import ThisMonthFilter, ThisWeekFilter, TodayFilter
from flask_admin.contrib.sqla.filters import DateBetweenFilter
from sqlalchemy import func
from datetime import datetime
class Dashboard(MyModelView):
    create_template = 'admin/reservation_form.html'
    list_template = 'admin/dashboard_list.html'
    can_create = False
    can_edit = False
    can_delete = False
    
    column_list = (
        'carwash.carwash_name',
        'car.license_plate',
        'reservation_date',
        'car.company.company_name',
        'service.service_name',
        'extras',
        'final_price',
    )

    column_labels = {
        'carwash.carwash_name': 'Hely',
        'reservation_date': 'Dátum',
        'car.license_plate': 'Rendszám',
        'service.service_name': 'Csomag',
        'extras': 'Extra',
        'final_price': 'Bevétel',
        'car.company.company_name': 'Cégnév'
    }

    form_excluded_columns = ['billing']

    column_filters = [
        TodayFilter(ReservationModel.reservation_date),
        ThisWeekFilter(ReservationModel.reservation_date),
        ThisMonthFilter(ReservationModel.reservation_date),
        DateBetweenFilter(ReservationModel.reservation_date, "Custom date"),
        'car.license_plate',
        'service.service_name',
        'carwash.carwash_name',
        'car.company.company_name',
    ]
        

    def render(self, template, **kwargs):
        if template == 'admin/dashboard_list.html':
            # Calculate sums
            self.get_sum('final_price')

            # Get revenue data
            dates, revenues = self.get_revenue_data()

            # Append summary data to kwargs
            kwargs['summary_data'] = [
                {
                    'title': 'Összeg (filtered)',
                    'service.service_name': self.get_service_sum(),
                    'extras': self.get_extra_sum(),
                    'final_price': self.get_sum('final_price'),
                    'dates': dates,         # Add dates for the chart
                    'revenues': revenues,   # Add revenues for the chart
                },
            ]

        return super(Dashboard, self).render(template, **kwargs)

    def get_revenue_data(self):
        # Query to get daily revenue data
        results = (
            self.query_all
            .with_entities(
                func.date(ReservationModel.reservation_date).label('date'),
                func.sum(ReservationModel.final_price).label('total_revenue')
            )
            .group_by(func.date(ReservationModel.reservation_date))
            .order_by(func.date(ReservationModel.reservation_date))  # Optional: order by date
            .all()
        )

        dates = [result[0] for result in results] 
        revenues = [result[1] if result[1] is not None else 0 for result in results] 

        dates = [datetime.strptime(date, '%Y-%m-%d') for date in dates]
        return dates, revenues
    
    
    def get_service_sum(self):
        query = self.query_all

        total_sum = 0
        for item in query:      
            try:      
                if not item.car.car_type:
                    current_app.logger.warning('Car without car type')
                elif item.car.car_type == CarTypeEnum.small_car:
                    total_sum += item.service.price_small
                elif item.car.car_type == CarTypeEnum.medium_car:
                    total_sum += item.service.price_medium
                elif item.car.car_type == CarTypeEnum.large_car:
                    total_sum += item.service.price_large
            except Exception as e:
                current_app.logger.error(f'Error processing item: {e}')
            
        return total_sum
    
    def get_extra_sum(self):
        query = self.query_all
        
        total_sum = 0
        for item in query:
            if item.extras:
                for extra in item.extras:
                    total_sum += extra.price
        
        return total_sum
                
            
    





