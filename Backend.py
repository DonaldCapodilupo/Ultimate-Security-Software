from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
from sqlalchemy_utils import database_exists, create_database
from getpass import getpass
import os

#Required Databases: Cases, People, Vehicles, Activity

def setup_Databases():
    # join the inputs into a complete database url.
    urls = ["sqlite+pysqlite:///Customers.db",
            "sqlite+pysqlite:///Cases.db",
            "sqlite+pysqlite:///Vehicles.db",
            "sqlite+pysqlite:///People of Interest.db"]

    for url in urls:
        # Create an engine object.
        engine = create_engine(url, echo=True)

        # Create database if it does not exist.
        if not database_exists(engine.url):
            create_database(engine.url)
            meta = MetaData()

            if "Customers" in url:
                new_table = Table(
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

                new_table = Table(
                    'Cases', meta,
                    Column('id', Integer, primary_key=True),
                    Column('case_number', String),
                    Column('investigation_type', String),

                )

            elif "Vehicles" in url:
                new_table = Table(
                    'Vehicles', meta,
                    Column('id', Integer, primary_key=True),
                    Column('address', String),
                    Column('manufacturer', String),
                    Column('model', String),
                    Column('color', String),
                    Column('license_plate_number', String),
                )

            elif "People" in url:
                new_table = Table(
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




def create_Case(customer, investigation_type):
    #Get input Case information. Customer - Investigation Type - Numeric Investigation

    investigation_types = {
        "Background Check":"BGCK",
        "Political Corruption": "POLCUR",
        "Gather Dirt":"INTEL"
    }

    case_num = 1

    #Create Case Number Based on case information.
    case_number = customer[0:3].upper() + "-" + investigation_types[investigation_type] + "-" + str(case_num)
    print("Creating Case Number: " + case_number)

    #Create a case folder. Within case folder create Images folder, DAR's, Relevant BOLO's, Witness statements, POI,
    os.mkdir(case_number)

    case_directories = ["Daily Activity Reports", "Witness Statements", "Images", "People of Interest",
                        "Vehicles of Interest", "External Evidence"]

    os.chdir(case_number)

    for directory in case_directories:
        os.mkdir(directory)
