from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, insert, inspect
from sqlalchemy_utils import database_exists, create_database
import os, sqlite3


def create_Case(case_number):
    # Get input Case information. Customer - Investigation Type - Numeric Investigation
    print("Creating Case Number: " + case_number)

    # Create a case folder. Within case folder create Images folder, DAR's, Relevant BOLO's, Witness statements, POI,
    os.mkdir(case_number)

    case_directories = ["Daily Activity Reports", "Witness Statements", "Images", "People of Interest",
                        "Vehicles of Interest", "External Evidence"]

    for directory in case_directories:
        os.mkdir(case_number + "/" + directory)


class Database_Modifier:
    def __init__(self, table_name):
        self.table_name = table_name

    def check_If_Table_Exists(self, list_of_columns):
        db = sqlite3.connect("Information.db")

        list_of_columns = [column.replace(" ","_") for column in list_of_columns]

        create_table_sql = f"CREATE TABLE IF NOT EXISTS {self.table_name} (id INTEGER PRIMARY KEY AUTOINCREMENT  , {', '.join([f'{col} TEXT' for col in list_of_columns])})"

        db.execute(create_table_sql)
        db.commit()

    def create_Database_Row(self, dict_of_values):
        db = sqlite3.connect("Information.db")

        columns = [column_name.replace(" ","_") for column_name in dict_of_values.keys()]
        values = [value.replace(" ","_") for value in dict_of_values.values()]

        insert_sql = f"INSERT INTO {self.table_name} ({', '.join(columns)}) VALUES ({', '.join(['?']*len(columns))})"


        db.execute(insert_sql, values)
        db.commit()

    def read_Database_Table(self, searched_name):
        import pandas as pd
        db_connection = 'sqlite+pysqlite:///Information.db'
        engine = create_engine(db_connection)
        conn = engine.connect()

        df = pd.read_sql('SELECT * FROM ' + self.table_name, conn,
                         )

        for index, row in df.iterrows():
            if row["BOLO_Person_Details_Name"] == searched_name:
                print(row)

    def update_Database_Table(self):
        pass

    def destroy_Database_Row(self, id_number):
        db = sqlite3.connect("Information.db")

        insert_sql = f"DELETE FROM {self.table_name} WHERE id = '{id_number}'"



        db.execute(insert_sql)
        db.commit()






