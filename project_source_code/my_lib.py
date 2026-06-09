#mylib.py
import sqlite3
class Database_Manager:
    def __init__(self,name: str):
        self.connection=sqlite3.connect(name)
        self.cursor=self.connection.cursor()
    def search_one(self,query,values):
        result=self.cursor.execute(query,values).fetchone()
        return result
    def search_all(self,query,values):
        result=self.cursor.execute(query,values).fetchall()
        return result
    def close(self):
        self.connection.close()
    def run_save(self,query,values):
        self.cursor.execute(query,values)
        self.connection.commit()
