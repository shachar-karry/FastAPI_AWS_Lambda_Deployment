import os
from tempfile import gettempdir


def get_connect_str(db_name=None):
    tmp_dir = gettempdir()
    sqlite_str = 'sqlite:///' + tmp_dir
    conn_str = os.getenv("MYSQL_CONNECTION_STR", sqlite_str)
    if db_name:
        conn_str += '/' + db_name
        if conn_str.startswith("sqlite"):
            conn_str += ".db"
    print("connect string:", conn_str)
    return conn_str
