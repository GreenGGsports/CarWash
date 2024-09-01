from flask_admin.contrib.sqla import ModelView
from flask import flash , current_app

class MyModelView(ModelView):
    def on_model_change(self, form, model, is_created):
        self.session = current_app.session_factory.get_session()
        try:
            self.session.add(model)
            self.session.commit()
        except Exception as  e :
            self.session.rollback()
            current_app.logger.error(e)

        # Call the parent class's on_model_change method
        super(MyModelView, self).on_model_change(form, model, is_created)
        self.session.close()

    def handle_view_exception(self, exc):
        flash(f'An unexpected error occurred: {exc}', 'error')
        return False
