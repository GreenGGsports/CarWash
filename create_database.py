from sqlalchemy import create_engine
from src.models.base import Base

def create_database():
    db_path = 'sqlite:///db/car_wash.db'
    engine = create_engine(db_path)
    Base.metadata.create_all(engine)
    print("Database created successfully.")

if __name__ == '__main__':
    create_database()