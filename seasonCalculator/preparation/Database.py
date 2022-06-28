import pyodbc
import pandas as pd


class DBConnection:
    # class variables shared by all instances
    instance = None
    server = "SW79P142\\SQL2019_DB"
    driver = "{SQL Server}"
    port = "1433"

    def __new__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super().__new__(DBConnection)
            return cls.instance
        return cls.instance

    # instance variables unique to each instance
    def __init__(self, database_name):
        self.database_name = database_name
        self.connection = pyodbc.connect('DRIVER=' + self.driver +
                                         ';SERVER=' + self.server +
                                         ';PORT=' + self.port +
                                         ';DATABASE=' + self.database_name)
        self.cursor = self.connection.cursor()

    def __del__(self):
        self.cursor.close()
        self.connection.close()
        pass

    # Functions for CRUD operations
    def load_data_by_statement(self, query):
        return pd.read_sql(query, self.connection)
