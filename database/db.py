from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from settings import settings

if settings.MODE == "DEV":
    database_url = settings.DB_URL
else:
    database_url = settings.TEST_DB_URL

Base = declarative_base()
engine = create_engine(database_url)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
