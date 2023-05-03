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


class HTML_To_Database:
    def __init__(self, table_name, dict_of_values):
        self.table_name = table_name
        self.dict_of_values = {column_title.replace(" ", "_"): value for column_title, value in dict_of_values.items()}
        self.db_connection = 'sqlite+pysqlite:///Information.db'


        #self.cur = self.con.cursor()
        #self.cur.execute("CREATE TABLE IF NOT EXISTS " + self.table_name + " (?)", parameters=["Money"])


        #Check if DB exists
        #If not, create one.
        #Chec if table exists
        #If not, creat one
        #inset values into table

    def check_If_Table_Exists(self):
        db = sqlite3.connect("Information.db")
        print(db)

        # Define the CREATE TABLE SQL statement
        create_table_sql = f"CREATE TABLE IF NOT EXISTS {self.table_name} (id INTEGER AUTO_INCREMENT PRIMARY KEY , {', '.join([f'{col} TEXT' for col in self.dict_of_values.keys()])})"

        db.execute(create_table_sql)
        db.commit()

    def create_Database_Row(self):
        db = sqlite3.connect("Information.db")

        insert_sql = f"INSERT INTO {self.table_name} ({', '.join(self.dict_of_values.keys())}) VALUES ({', '.join(['?']*len(self.dict_of_values.keys()))})"

        values = [value for value in self.dict_of_values.values()]

        db.execute(insert_sql, values)
        db.commit()

    def remove_Database_Row(self):
        db = sqlite3.connect("Information.db")

        insert_sql = f"DELETE FROM {self.table_name} WHERE Cats = 'Chester'"



        db.execute(insert_sql)
        db.commit()


HTML_To_Database("Customers",{"Name":"","Birthdate":"","Eye Color":""}).check_If_Table_Exists()
HTML_To_Database("Customers",{"Name":"Ryan","Birthdate":"09/13/1993","Eye Color":"Green"}).create_Database_Row()
HTML_To_Database("Customers",{"Name":"","Birthdate":"","Eye Color":""}).remove_Database_Row()



#
# print(insp.has_table(self.table_name))
# if not insp.has_table(self.table_name):
#
#
#    conn.execute(
#        "CREATE TABLE "+ self.table_name
#    )
#
#
# table = Table(
#    self.table_name, meta_data,
#    Column('id', Integer, primary_key=True),
#    *(Column(rowname.replace(" ", "_"), String()) for rowname in dict_of_values.keys()),
#
# )
#
#
## Create database if it does not exist.
# if not database_exists(engine.url):
#    meta_data.create_all(engine)
#
#
# stmt = (
#    insert(table).
#        values(self.dict_of_values)
# )
# conn.execute(stmt)
# conn.commit()




def read_Database(database_name, searched_name, desired_results):
    import pandas as pd
    db_connection = 'sqlite+pysqlite:///Information.db'
    engine = create_engine(db_connection)
    conn = engine.connect()

    df = pd.read_sql('SELECT * FROM ' + database_name, conn,
                     )

    for index, row in df.iterrows():
        if row["BOLO_Person_Details_Name"] == searched_name:
            print(row)
