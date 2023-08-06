import sqlite3
import os
from chrome_spider.common.config import config

create_table_account = '''
create table account(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name varchar(200),
    phone_number varchar(200),
    password varchar(200),
    cookie varchar(1000),
    host varchar(10)
);
'''


# mkdir ~/.flow-track
class DB():
    def __init__(self):
        db_name = config.db_name
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    def __enter__(self):
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.commit()
        self.cursor.close()
        self.conn.close()

def init_table():
    with DB() as cursor:
        cursor.execute(create_table_account)
        

        
if __name__ == "__main__":
    with DB() as cursor:
        init_table()
