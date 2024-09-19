from sqlalchemy.orm import scoped_session, sessionmaker
class SessionFactory:
    def __init__(self, engine):
        # Create a sessionmaker bound to the engine
        self.session_factory = sessionmaker(bind=engine)
        # Create a scoped session using the sessionmaker
        self.Session = scoped_session(self.session_factory)
        
    def get_session(self):
        # Return the scoped session instance
        return self.Session
        
    def remove(self, exception = None):
        # Remove the current scoped session
        if exception: 
            self.Session.rollback()
        self.Session.remove()