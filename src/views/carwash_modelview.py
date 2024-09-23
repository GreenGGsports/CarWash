from src.views.my_modelview import MyModelView
from wtforms import TimeField, IntegerField, DateTimeField
from wtforms.validators import DataRequired
from flask import flash, current_app

class CarwashAdminView(MyModelView):
    form_extra_fields = {
        'start_time': TimeField('Nyitás', validators=[DataRequired()]),
        'end_time': TimeField('Zárás', validators=[DataRequired()]),
    }

    form_excluded_columns = ['slots']
    
    column_labels = {
        'carwash_name': 'Név',
        'location': 'Helyszín',
        'image_name': 'Kép',
        'close_start': 'Tiltás (-tól)',
        'close_end': 'Tiltás (-ig)',
        'start_time': 'Nyitás',
        'end_time': 'Zárás',
        'capacity': 'Kapacitás',  # A slot_count nevének megjelenítése
    }

    def on_model_change(self, form, model, is_created):
        """
        A modell elmentése előtt meghívjuk a megfelelő slot kezelési metódust,
        attól függően, hogy új létrehozásról vagy frissítésről van szó.
        """
        try:
            if is_created:
                # Először mentsük el a carwash-t
                self.session.add(model)
                self.session.commit()  # Először commit, hogy a model.id elérhető legyen

                # Ezután hozd létre a slotokat
                model.create_default_slots(
                    session=self.session,  # AdminView által biztosított session
                    start_time=form.start_time.data,
                    end_time=form.end_time.data,
                    slot_count=model.capacity,
                )
                flash(f'Slots successfully created for {model.carwash_name}', 'success')
            else:
                # Ha egy meglévő Carwash-t frissítünk, akkor update_default_slots
                model.update_default_slots(
                    session=self.session,
                    start_time=form.start_time.data,
                    end_time=form.end_time.data,
                    slot_count =model.capacity
                )
                flash(f'Slots successfully updated for {model.carwash_name}', 'success')
        except Exception as e:
            flash(f'Error during slot handling: {str(e)}', 'error')
            current_app.logger.error(e)
            self.session.rollback()
            raise
