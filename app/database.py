from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
from psycopg2.extras import RealDictCursor
from .config import setting

SQLALCHEMY_DATABASE_URL =f'postgresql://{setting.database_username}:{setting.database_password}@{setting.database_hostname}:{setting.database_port}/{setting.database_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal=sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


while True:
    try: 
        conn =psycopg2.connect(host='dpg-cj38k7enqql8v0f6pao0-a', database ='mydb_zs8r', user='mydb_zs8r_user', password='XxVMo8UdTjfl0r8c0KpR3gqdMyM1rYHM', cursor_factory=RealDictCursor )
        cursor = conn.cursor()
        print('database connection was successful)
        break 
    except Exception as error:
        print("connection was error")
        print ("Error ", error)
        
