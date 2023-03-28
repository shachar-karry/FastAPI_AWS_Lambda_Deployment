import sqlalchemy
from dotenv import load_dotenv, find_dotenv

from db_utils import get_connect_str

load_dotenv(find_dotenv())

# create a SQLAlchemy engine and sessionmaker
connect_string = get_connect_str()

engine = sqlalchemy.create_engine(connect_string)  # connect to server

from sqlalchemy import text
with engine.connect() as connection:
    result = connection.execute(text("CREATE DATABASE users"))
#engine.execute("CREATE DATABASE users")  #create db
#engine.execute("USE users")  # select new db