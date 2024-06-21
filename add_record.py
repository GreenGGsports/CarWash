from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.models.reservation_model import Reservation
import datetime

# Assuming you have created the database and engine as before
db_path = 'sqlite:///db/car_wash.db'

# Create the database engine
engine = create_engine(db_path)
# Function to create a session
def create_session():
    Session = sessionmaker(bind=engine)
    return Session()

# Example usage
if __name__ == '__main__':
    session = create_session()
    
    # Create a new reservation
    new_reservation = Reservation.create_reservation(
        session,
        appointment=datetime.datetime.utcnow(),
        license_plate='ABC123',
        name='John Doe',
        phone_number='123-456-7890',
        brand='Toyota',
        type='Sedan',
        company_id=1,
        service_id=1,
        parking_spot='A1'
    )   
    
    session.close()
