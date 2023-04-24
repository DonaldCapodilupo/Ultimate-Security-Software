from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, insert
from sqlalchemy_utils import database_exists, create_database
import os

def setup_Databases():
    # join the inputs into a complete database url.
    urls = ["sqlite+pysqlite:///Customers.db",
            "sqlite+pysqlite:///Cases.db",
            "sqlite+pysqlite:///Vehicles.db",
            "sqlite+pysqlite:///People of Interest.db",
            "sqlite+pysqlite:///BOLOs.db"]

    for url in urls:
        # Create an engine object.
        engine = create_engine(url, echo=True)

        # Create database if it does not exist.
        if not database_exists(engine.url):
            create_database(engine.url)
            meta = MetaData()

            if "Customers" in url:
                customers_table = Table(
                    'Customer', meta,
                    Column('id', Integer, primary_key=True),
                    Column('first_name', String),
                    Column('last_name', String),
                    Column('phone_number', String),
                    Column('email', String),
                    Column('employer', String),
                    Column('address', String),
                    Column('state', String),
                    Column('zip', String),
                    Column('employer_is_customer', String),
                    Column('employer_address', String),
                    Column('employer_phone_number', String),
                    Column('employed_since', String),
                    Column('job_title', String),
                )

            elif "Cases" in url:

                cases_table  = Table(
                    'Cases', meta,
                    Column('id', Integer, primary_key=True),
                    Column('customer', String),
                    Column('case_number', String),
                    Column('investigation_type', String),

                )

            elif "Vehicles" in url:
                vehicles_table = Table(
                    'Vehicles', meta,
                    Column('id', Integer, primary_key=True),
                    Column('address', String),
                    Column('manufacturer', String),
                    Column('model', String),
                    Column('color', String),
                    Column('license_plate_number', String),
                )

            elif "BOLOs" in url:
                bolo_table = Table(
                    'BOLOs', meta,
                    Column('id', Integer, primary_key=True),
                    Column('name', String),
                    Column('alias', String),
                    Column('DOB', String),
                    Column('sex', String),
                    Column('race', String),
                    Column('ethnicity', String),
                    Column('height', String),
                    Column('weight', String),
                    Column('hair', String),
                    Column('eyes', String),
                    Column('DLB', String),
                    Column('SSN', String),
                    Column('LKA', String),
                    Column('know_associates', String),
                    Column('vehicle_make', String),
                    Column('vehicle_model', String),
                    Column('vehicle_color', String),
                    Column('vehicle_LKA', String),
                    Column('vehicle_notable_markings', String),
                    Column('vehicle_date_last_seen', String),
                    Column('vehicle_considered_dangerous', String),
                    Column('vehicle_owner', String),
                    Column('vehicle_VIN', String),


                )

            elif "People" in url:
                people_table = Table(
                    'People', meta,
                    Column('id', Integer, primary_key=True),
                    Column('last_name', String),
                    Column('first_name', String),
                    Column('middle_name', String),
                    Column('home_address', String),
                    Column('city', String),
                    Column('state', String),
                    Column('phone_number', String),
                    Column('drivers_license_number', String),
                    Column('marital_status', String),
                    Column('date_of_birth', String),
                    Column('place_of_birth', String),
                    Column('age', String),
                    Column('sex', String),
                    Column('race', String),
                    Column('height', String),
                    Column('weight', String),
                    Column('hair_color', String),
                    Column('eye_color', String),
                    Column('shoe_size', String),
                    Column('dominant_hand', String),
                    Column('disability', String),
                    Column('scars_marks_tattoos', String),
                    Column('prior_military_experience', String),
                    Column('martial_arts_experience', String),
                    Column('firearm_owner', String),
                    Column('prior_arrests', String),
                    Column('prior_felonies', String),
                    Column('outstanding_warrants', String),
                    Column('currently_under_investigation', String),
                    Column('employer', String),
                    Column('employer_phone', String),
                    Column('employer_address', String),
                    Column('length_of_employment', String),
                    Column('occupation', String),

                )

            meta.create_all(engine)
        else:
            # Connect the database if exists.
            engine.connect()




def create_Case_Database_Row(customer, investigation_type, case_number):
    meta_data = MetaData()
    cases_table = Table(
        'Cases', meta_data,
        Column('id', Integer, primary_key=True),
        Column('customer', String),
        Column('case_number', String),
        Column('investigation_type', String),

    )

    # db_connection = 'mysql+pymysql://username:pasword@hostname/db_name'

    db_connection = 'sqlite+pysqlite:///Cases.db'
    engine = create_engine(db_connection)

    try:

        conn = engine.connect()

        print('db connected')

        print('connection object is :{}'.format(conn))

    except:

        print('db not connected')

    meta_data.create_all(engine)

    stmt = (
        insert(cases_table).
            values(customer=customer, investigation_type=investigation_type,case_number=case_number )
    )
    conn.execute(stmt)
    conn.commit()
    #with create_engine("sqlite+pysqlite:///Cases.db", ).connect() as conn:
    #    result = conn.execute(

def create_BOLO_Database_Row(data_dict):
    meta_data = MetaData()
    bolo_table = Table(
        'BOLOs', meta,
        Column('id', Integer, primary_key=True),
        Column('name', String),
        Column('alias', String),
        Column('DOB', String),
        Column('sex', String),
        Column('race', String),
        Column('ethnicity', String),
        Column('height', String),
        Column('weight', String),
        Column('hair', String),
        Column('eyes', String),
        Column('DLB', String),
        Column('SSN', String),
        Column('LKA', String),
        Column('know_associates', String),
        Column('vehicle_make', String),
        Column('vehicle_model', String),
        Column('vehicle_color', String),
        Column('vehicle_LKA', String),
        Column('vehicle_notable_markings', String),
        Column('vehicle_date_last_seen', String),
        Column('vehicle_considered_dangerous', String),
        Column('vehicle_owner', String),
        Column('vehicle_VIN', String),)

    db_connection = 'sqlite+pysqlite:///BOLOs.db'
    engine = create_engine(db_connection)

    try:

        conn = engine.connect()

        print('db connected')

        print('connection object is :{}'.format(conn))

    except:

        print('db not connected')

    meta_data.create_all(engine)

    stmt = (
        insert(bolo_table).
            values(customer=customer, investigation_type=investigation_type, case_number=case_number)
    )
    conn.execute(stmt)
    conn.commit()


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

        print(self.dict_of_values)


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

