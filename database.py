from sqlalchemy import create_engine
from src.models.base import BaseModel
from src.models.billing_model import BillingModel
from src.models.reservation_model import ReservationModel
from src.models.service_model import ServiceModel
from src.models.company_model import CompanyModel
from src.models.slot_model import SlotModel
from src.models.user_model import UserModel
from src.models.carwash_model import CarWashModel
from src.models.extra_model import ExtraModel
from src.models.reservation_extras import reservation_extra
from src.models.customer_model import CustomerModel
from src.models.car_model import CarModel

from sqlalchemy import text  # Import the text function for executing raw SQL queries
from sqlalchemy.exc import SQLAlchemyError 
import os 
import sqlalchemy


def create_database(engine):
    BaseModel.metadata.create_all(engine)
    print("Database created successfully.")

def check_database_connection(engine, app):
    """
    Check if the SQLAlchemy engine is properly connected to the database.
    
    Parameters:
        engine: SQLAlchemy Engine instance.
        app: Flask app instance for logging.

    Returns:
        bool: True if the connection is successful, False otherwise.
    """
    try:
        # Attempt to connect and execute a simple query
        with engine.connect() as connection:
            # Use the 'text' function to execute a raw SQL query
            result = connection.execute(text("SELECT 1"))
            app.logger.debug(f"Database connection check result: {result.fetchone()}")
        return True
    except SQLAlchemyError as e:
        # Log any errors that occur during the connection check
        app.logger.error(f"Database connection failed: {e}")
        return False
    
def connect_unix_socket() -> sqlalchemy.engine.base.Engine:
    """Initializes a Unix socket connection pool for a Cloud SQL instance of MySQL."""
    
    # Fetch database connection parameters from environment variables
    try:
        db_user = os.environ["DB_USER"]  # e.g. 'my-database-user'
        db_pass = os.environ["DB_PASSWORD"]  # e.g. 'my-database-password'
        db_name = os.environ["DB_NAME"]     # e.g. 'my-database'
        
        # Construct the Unix socket path
        unix_socket_path = f"/cloudsql/winged-moon-431714-f5:europe-central2:cwsandbox"
        
        # For logging and debugging
        print(f"Connecting to database '{db_name}' with user '{db_user}' at '{unix_socket_path}'")
    
    except KeyError as e:
        raise EnvironmentError(f"Missing required environment variable: {e}")

    # Create a SQLAlchemy Engine using a connection pool
    pool = sqlalchemy.create_engine(
            # Equivalent URL:
            # mysql+pymysql://<db_user>:<db_pass>@/<db_name>?unix_socket=<socket_path>/<cloud_sql_instance_name>
            sqlalchemy.engine.url.URL.create(
                drivername="mysql+pymysql",
                username=db_user,
                password=db_pass,
                database=db_name,
                query={"unix_socket": unix_socket_path},
            ),
            # ...
        )
    return pool
    
if __name__ == '__main__':
    create_database()
    