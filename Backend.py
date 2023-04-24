from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, insert
from sqlalchemy_utils import database_exists, create_database
import os


def create_Case(case_number):
        # Get input Case information. Customer - Investigation Type - Numeric Investigation
        print("Creating Case Number: " + case_number)

        # Create a case folder. Within case folder create Images folder, DAR's, Relevant BOLO's, Witness statements, POI,
        os.mkdir(case_number)

        case_directories = ["Daily Activity Reports", "Witness Statements", "Images", "People of Interest",
                            "Vehicles of Interest", "External Evidence"]

        os.chdir(case_number)

        for directory in case_directories:
            os.mkdir(directory)



class HTML_To_Database:
    def __init__(self, table_name, dict_of_values):
        self.table_name = table_name
        self.dict_of_values = {column_title.replace(" ","_"): value for column_title, value in dict_of_values.items()}
        meta_data = MetaData()

        db_connection = 'sqlite+pysqlite:///'+self.table_name+'.db'
        engine = create_engine(db_connection)

        table = Table(
            self.table_name, meta_data,
            Column('id', Integer, primary_key=True),
            *(Column(rowname.replace(" ","_"), String()) for rowname in dict_of_values.keys()),

        )


        # Create database if it does not exist.
        if not database_exists(engine.url):
            meta_data.create_all(engine)

        conn = engine.connect()

        stmt = (
            insert(table).
                values(self.dict_of_values)
        )
        conn.execute(stmt)
        conn.commit()

