'''
    Este archivo permite conectar con la base de datos
'''
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "mysql://root:127.0.0.1:3307/autolavadoDB"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
sessionLocal = sessionmaker(autocommit = False, autoflush = False, bind = engine)
Base = declarative_base()


