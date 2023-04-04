import os

import boto3
from botocore.exceptions import NoRegionError
from fastapi import FastAPI
from mangum import Mangum
from pydantic import BaseModel


from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

from dotenv import load_dotenv, find_dotenv

import sys
sys.path.append('..')
from utils.db_utils import get_connect_str


app = FastAPI()

load_dotenv(find_dotenv())

# create a SQLAlchemy engine and sessionmaker
connect_string = get_connect_str("users", env_var="POSTGRESQL_CONNECTION_STR")
engine = create_engine(connect_string, echo=os.getenv("DEBUG_ECHO_SQL", False))

print("Engine created")

Session = sessionmaker(bind=engine)

# define a SQLAlchemy model for user registration
Base = declarative_base()

sns_client = None


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(64), unique=True, index=True)
    password = Column(String(64))


# create the users table if it doesn't exist
Base.metadata.create_all(bind=engine)
print("Create all Completed")


# define a Pydantic model for user registration
class UserRegistration(BaseModel):
    username: str
    password: str


# define a route for user registration
@app.post("/users")
def register_user(user: UserRegistration):
    # create a new user object
    db_user = User(username=user.username, password=user.password)

    # add the user to the database
    session = Session()
    session.add(db_user)
    session.commit()
    if sns_client:
        sns_client.publish(PhoneNumber="+972523370403", Message=f"New user registered successfully: {user.username}")

    return {"message": "User registered successfully"}


# define a route for retrieving all users
@app.get("/users")
def get_users():
    print("Called get_users")
    session = Session()

    # retrieve all users from the database
    users = session.query(User.id, User.username, User.password).all()

    # format the users as a list of dicts
    user_dicts = [{"id": id,
                   "username": username,
                   "password": '*'*(len(password)-3) + password[-3:]}
                  for id, username, password in users]

    return {"users": user_dicts}


# define a route for health check
@app.get("/health")
def get_users():
    print("Called health_check")
    session = Session()

    # retrieve all users from the database
    user = session.query(User.id, User.username, User.password).first()
    assert len(user) > 2
    assert type(user[0]) is int
    return {"message": "healthy"}


# sns sanity + cold start indication
if os.getenv("PUBLISH_ON_INIT", False):
    print("Attempting SNS")
    try:
        sns_client = boto3.client("sns")
        print("SNS client initialized")
        #if os.name != "nt":
        sns_client.publish(PhoneNumber="+972523370403", Message=f"New lambda cold start 4")
    except NoRegionError as error:
        print("sns_client error:", error)
        pass


print("Initializing handler")

handler = Mangum(app=app)
