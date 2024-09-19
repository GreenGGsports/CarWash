from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
import os
import sqlalchemy
from flask import g, current_app

def connect_tcp_socket() -> sqlalchemy.engine.base.Engine:
    """Initializes a TCP connection pool for a MySQL instance."""
    try:
        db_user = os.environ["DB_USER"]
        db_pass = os.environ["DB_PASSWORD"]
        db_name = os.environ["DB_NAME"]
        db_host = os.environ["DB_HOST"]
        db_port = int(os.environ.get("DB_PORT", 3306))
        
        print(f"Connecting to database '{db_name}' at '{db_host}:{db_port}'")
    
    except KeyError as e:
        raise EnvironmentError(f"Missing required environment variable: {e}")

    engine = sqlalchemy.create_engine(
        sqlalchemy.engine.url.URL.create(
            drivername="mysql+pymysql",
            username=db_user,
            password=db_pass,
            host=db_host,
            port=db_port,
            database=db_name
        ),
        pool_size=1,
        max_overflow=0,
        pool_timeout=30,
        pool_recycle=600,  # Recycle connections every 10 minutes
        pool_pre_ping=True,  # Ping connections before using them
    )

    # Set session timeout values
    try:
        with engine.connect() as connection:
            connection.execute(text("SET SESSION wait_timeout=60"))
            connection.execute(text("SET SESSION interactive_timeout=60"))
            print("MySQL timeout values set: wait_timeout=60, interactive_timeout=60")
    except SQLAlchemyError as e:
        print(f"Error setting MySQL timeout: {e}")

    return engine

def get_db():
    """Get or create the database connection."""
    if 'db' not in g:
        g.db = connect_tcp_socket()
    return g.db

def close_db(e=None):
    """Close the database connection after each request."""
    db = g.pop('db', None)
    if db is not None:
        db.dispose()

def check_database_connection(engine, app):
    """Check if the engine can connect to the database."""
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            print(f"Connection check result: {result.fetchone()}")
        return True
    except SQLAlchemyError as e:
        current_app.logger.error(f"Database connection failed: {e}")
        return False