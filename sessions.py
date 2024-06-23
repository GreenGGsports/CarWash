from sqlalchemy.orm import sessionmaker
class SessionFactory:
    def __init__(self, engine):
        self.Session = sessionmaker(bind=engine)
        
    def get_session(self):
        return self.Session()