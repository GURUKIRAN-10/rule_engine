from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = 'sqlite:///rules.db'  # SQLite database for simplicity

Base = declarative_base()
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Rule(Base):
    __tablename__ = 'rules'

    id = Column(Integer, primary_key=True, index=True)
    rule_string = Column(String, index=True)

def get_session():
    return SessionLocal()

# Create the database tables if they don't exist
Base.metadata.create_all(bind=engine)
