from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

class DatabaseHelper():
    def __init__(self, conn_str):
        self.engine = create_engine(conn_str, echo=True)