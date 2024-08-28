from flask_admin.contrib.sqla import ModelView
from flask import flash

class MyModelView(ModelView):
    def on_model_change(self, form, model, is_created):
        try:
            self.session.add(model)
            self.session.commit()
        except Exception :
            self.session.rollback()

        # Call the parent class's on_model_change method
        super(MyModelView, self).on_model_change(form, model, is_created)

    def handle_view_exception(self, exc):
        flash(f'An unexpected error occurred: {exc}', 'error')
        return False
