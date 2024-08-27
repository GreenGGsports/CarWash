from flask_admin.contrib.sqla import ModelView
from flask import flash

class MyModelView(ModelView):
    def on_model_change(self, form, model, is_created):
        try:
            super(MyModelView, self).on_model_change(form, model, is_created)
            self.session.commit()

        except Exception as e:
            self.session.rollback()
            flash(f'An error occurred: {e}', 'error')
            return False

    def handle_view_exception(self, exc):
        flash(f'An unexpected error occurred: {exc}', 'error')
        return False 
