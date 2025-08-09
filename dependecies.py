from models import User, db
from sqlalchemy.orm import sessionmaker

def take_session():
    try:
        Session = sessionmaker(bind=db)
        session = Session()

        yield session
    finally:
        session.close()