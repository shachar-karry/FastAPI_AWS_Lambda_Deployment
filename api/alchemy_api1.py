from fastapi import FastAPI
from mangum import Mangum
from pydantic import BaseModel


from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

from dotenv import load_dotenv, find_dotenv

from db_utils import get_connect_str


app = FastAPI()

load_dotenv(find_dotenv())

# create a SQLAlchemy engine and sessionmaker
connect_string = get_connect_str("users")
engine = create_engine(connect_string)

print("Engine created")

Session = sessionmaker(bind=engine)

print("Session created")

# define a SQLAlchemy model for user registration
Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(64), unique=True, index=True)
    password = Column(String(64))


# create the users table if it doesn't exist
print("Create all")
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

print("Creating app")
handler = Mangum(app=app)
