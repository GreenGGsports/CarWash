from flask_admin.contrib.sqla import ModelView

class ServiceModelView(ModelView):
    column_labels = {
        'carwash.carwash_name': 'Car Wash Name',
        'service_name': 'Service Name',
        'price_small': 'Price (Small)',
        'price_large': 'Price (Large)'
    }

    column_list = ['carwash.carwash_name', 'service_name', 'price_small', 'price_large']