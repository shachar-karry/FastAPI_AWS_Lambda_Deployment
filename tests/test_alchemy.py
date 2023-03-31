from fastapi.testclient import TestClient
from api.alchemy_api1 import app

import sqlalchemy
from dotenv import load_dotenv, find_dotenv

import os


# def test_mysql_db():
#     load_dotenv(find_dotenv())
#     # create a SQLAlchemy engine and sessionmaker
#     conn_str = os.getenv("MYSQL_CONNECTION_STR")
#     engine = sqlalchemy.create_engine(conn_str, echo=True)  # connect to server
#     print()
#     print(engine)
#
#
# def test_health():
#     client = TestClient(app)
#     response = client.get("/health")
#     assert response.status_code == 200
#     assert response.json() == {"message": "healthy"}
