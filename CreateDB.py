import sqlalchemy
from dotenv import load_dotenv, find_dotenv

from api.db_utils import get_connect_str

from sqlalchemy import text

load_dotenv(find_dotenv())

# create a SQLAlchemy engine and sessionmaker
connect_string = get_connect_str(env_var="POSTGRESQL_CONNECTION_STR")

engine = sqlalchemy.create_engine(connect_string, connect_args={'connect_timeout': 10})  # connect to server

with engine.connect() as connection:
    result = connection.execute(text("SELECT datname FROM pg_catalog.pg_database;"))
    [print(i) for i in result]

#     print(result)
#engine.execute("CREATE DATABASE users")  #create db
#engine.execute("USE users")  # select new db