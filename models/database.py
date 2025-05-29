from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./library.db"

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL, echo=False)

# Create a configured "Session" class
sessionalocal = sessionmaker(autocommit = False, autoflush = False, bind=engine)

# Create a base class for declarative models
Base = declarative_base()

def get_db_session():

    return sessionalocal()
def init_database():
    
    Base.metadata.create_all(bind=engine)