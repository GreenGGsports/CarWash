from flask_admin.contrib.sqla import ModelView
from flask import flash

class MyModelView(ModelView):
    def on_model_change(self, form, model, is_created):
        try:
            # Eredeti művelet végrehajtása
            super(MyModelView, self).on_model_change(form, model, is_created)
            # Tranzakció commit-álása, ha minden rendben van
            self.session.commit()
        except Exception as e:
            # Hibakezelés: visszagörgetjük a tranzakciót
            from pdb import set_trace
            set_trace()
            self.session.rollback()
            # Session lezárása
            self.session.close()
            # Flash üzenet a felhasználónak a hibáról
            flash(f'An error occurred: {e}', 'error')
            # Session újraindítása (opcionális, ha szükséges új session)
            self.session = self.create_session()  # Egyéni metódus az új session létrehozásához
            from pdb import set_trace
            set_trace()
            return False
    def handle_view_exception(self, exc):
        # Ha kivétel történik, ne dobjuk fel a hibaoldalt
        flash(f'An unexpected error occurred: {exc}', 'error')
        # A meglevő flash üzenetek törlése, hogy a hibás sikerüzenetek eltűnjenek
        self.session.pop('_flashes', None)
        return False  # Megakadályozza a hibaoldal megjelenítését

    def create_session(self):
        """Kezel egy új session létrehozását, ha szükséges"""
        from sqlalchemy.orm import sessionmaker
        engine = self.get_engine()  # Az engine szerzése a flask admin-ból
        Session = sessionmaker(bind=engine)
        return Session()
    
    def get_engine(self):
        """Visszaadja az SQLAlchemy engine-t"""
        return self.session.bind
