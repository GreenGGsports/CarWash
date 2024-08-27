from flask_admin.contrib.sqla import ModelView
from flask import flash
from sqlalchemy.exc import SQLAlchemyError

class MyModelView(ModelView):
    def on_model_change(self, form, model, is_created):
        # Temporarily disable autoflush
        self.session.autoflush = False

        try:
            # Execute the original operation
            super(MyModelView, self).on_model_change(form, model, is_created)
            # Manually flush and commit if no errors occur
            self.session.flush()
            self.session.commit()
        except SQLAlchemyError as e:
            # Handle SQLAlchemy errors
            if not self.session.is_active:
                self.session.rollback()  # Rollback if the session is not active
            flash(f'An error occurred: {e}', 'error')
            return False
        except Exception as e:
            # Handle other exceptions
            if not self.session.is_active:
                self.session.rollback()  # Rollback if the session is not active
            flash(f'An unexpected error occurred: {e}', 'error')
            return False
        finally:
            # Restore autoflush setting
            self.session.autoflush = True

    def handle_view_exception(self, exc):
        flash(f'An unexpected error occurred: {exc}', 'error')
        return False
