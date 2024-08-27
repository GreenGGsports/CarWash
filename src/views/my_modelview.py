from flask_admin.contrib.sqla import ModelView
from flask import flash

class MyModelView(ModelView):
    def on_model_change(self, form, model, is_created):
        # Session konfigurálása autoflush nélkül
        self.session.autoflush = False

        try:
            # Eredeti művelet végrehajtása
            super(MyModelView, self).on_model_change(form, model, is_created)
            
        except Exception as e:
            # Hibakezelés: visszagörgetjük a tranzakciót
            self.session.rollback()
            flash(f'An unexpected error occurred: {e}', 'error')
            return False
        finally:
            # Manuális flush és commit a végén
            self.session.flush()
            self.session.commit()
            # Session autoflush visszaállítása alapértelmezett állapotba
            self.session.autoflush = True

    def handle_view_exception(self, exc):
        flash(f'An unexpected error occurred: {exc}', 'error')
        return False
