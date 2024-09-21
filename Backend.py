import os, sqlite3
import requests
from bs4 import BeautifulSoup


def create_Case(case_number):
    # Get input Case information. Customer - Investigation Type - Numeric Investigation
    print("Creating Case Number: " + case_number)

    if "Open Cases" not in os.listdir():
        os.mkdir("Open Cases")

    # Create a case folder. Within case folder create Images folder, DAR's, Relevant BOLO's, Witness statements, POI,
    os.mkdir("Open Cases/" + case_number)

    case_directories = ["Daily Activity Reports", "Witness Statements", "Images", "People of Interest",
                        "Vehicles of Interest", "External Evidence"]

    for directory in case_directories:
        os.mkdir("Open Cases/" + case_number + "/" + directory)


def save_Admin_Form_Data(form_data, customer, report_type):
    import json, datetime

    data = {}

    os.mkdir("Admin/" + customer)

    for key, value in form_data.items():
        data[key] = value

    with open("Admin/" + customer + "/" + report_type + '.json', 'w') as f:
        json.dump(data, f)


def create_License_Plate_Image(plate_num):
    htmldata = requests.get(
        "https://www.acme.com/licensemaker/licensemaker.cgi?state=Massachusetts&text=" + plate_num + "&plate=1988&r=1675049699").text
    soup = BeautifulSoup(htmldata, 'html.parser')
    image = soup.find_all('img')[2].get("src")

    data = requests.get("https://www.acme.com/licensemaker/" + image).content

    # Opening a new file named img with extension .jpg
    # This file would store the data of the image file
    f = open(plate_num + '.jpg', 'wb')

    # Storing the image data inside the data variable to the file
    f.write(data)
    f.close()


def license_Plate_Capture():
    while "Screenshot_.png" not in os.listdir('static/images'):
        continue


def control_OBS_Zoom(zoom_value):
    import json, time
    import websocket
    ws = websocket.WebSocket()

    ws.connect("ws://192.168.0.24:8888/websocket")

    ws.send(json.dumps({"messageType": "setDeviceConfiguration",
                        "content": "{\"shutterSpeed\":{\"title\":\"1 / 30\",\"value\":0.029999999329447746},\"zoomLevelMin\":1,\"exposureEVmax\":8,\"isTorchAvailable\":true,\"isDevicePreviewOn\":true,\"temperature\":3500,\"deviceName\":\"iPhone\",\"resolutions\":[\"4032x3024\",\"3264x2448\",\"3840x2160\",\"2592x1944\",\"1920x1440\",\"1440x1080\",\"1920x1080\",\"1024x768\",\"1280x720\",\"960x540\",\"640x480\",\"480x360\",\"352x288\",\"192x144\"],\"isAutomaticWhiteBalanceModeEnabled\":true,\"isCustomExposureModeSupported\":true,\"isCustomWhiteBalanceModeSupported\":true,\"isoMin\":24,\"temperatureMin\":1800,\"resolution\":\"1280x720\",\"shutterSpeeds\":[{\"title\":\"1.0\",\"value\":1},{\"title\":\"1 / 2.0\",\"value\":0.5},{\"title\":\"1 / 4.0\",\"value\":0.25},{\"title\":\"1 / 8.0\",\"value\":0.12999999523162842},{\"title\":\"1 / 15\",\"value\":0.07000000029802322},{\"title\":\"1 / 30\",\"value\":0.029999999329447746},{\"title\":\"1 / 50\",\"value\":0.019999999552965164},{\"title\":\"1 / 100\",\"value\":0.009999999776482582}],\"focusConfiguration\":{\"lensPosition\":0.384313702583313,\"isLockedFocusModeSupported\":true,\"isSmoothAutoFocusSupported\":true,\"maxLensPosition\":1,\"isAutoFocusSupported\":true,\"crosshairMode\":{\"combined\":null},\"isContinuousAutoFocusSupported\":true,\"focusMode\":{\"auto\":0},\"isLockingFocusWithCustomLensPositionSupported\":true,\"isFocusPointOfInterestSupported\":true,\"minLensPosition\":0,\"isSmoothAutoFocusEnabled\":false,\"isAdjustingFocus\":false,\"isAutoFocusRangeRestrictionSupported\":true},\"iso\":800,\"isTorchEnabled\":false,\"lightingMode\":\"automatic\",\"framerates\":[\"24\",\"25\",\"30\",\"60\",\"120\",\"240\"],\"batteryState\":{\"charging\":{\"batteryLevel\":1}},\"cameras\":[{\"id\":\"com.apple.avfoundation.avcapturedevice.built-in_video:1\",\"title\":\"Front Wide Angle Camera\",\"position\":2},{\"id\":\"com.apple.avfoundation.avcapturedevice.built-in_video:0\",\"title\":\"Wide Angle Camera\",\"position\":1}],\"isoMax\":2304,\"zoomLevel\":" + str(
                            zoom_value) + ",\"zoomLevelMax\":24,\"exposureEVmin\":-8,\"exposureEV\":0.5,\"selectedCamera\":{\"id\":\"com.apple.avfoundation.avcapturedevice.built-in_video:0\",\"title\":\"Wide Angle Camera\",\"position\":1},\"isFrontCameraMirrored\":true,\"framerate\":\"30\",\"temperatureMax\":8000}"}))
    time.sleep(.5)
    print(ws.recv())

    ws.close()


def get_OBS_Zoom():
    import websocket, json
    ws = websocket.WebSocket()

    ws.connect("ws://192.168.86.250:8888//websocket")
    zoom_level = round(json.loads(json.loads(ws.recv())["content"])["zoomLevel"])

    return zoom_level


def open_Secret_Compartment():
    import pyfirmata

    import time

    board = pyfirmata.Arduino('COM3')

    while True:
        board.digital[13].write(1)

        time.sleep(1)

        board.digital[13].write(0)
        time.sleep(1)


def lookup_registration_info():
    import requests

    import uncurl

    # input()
    # URL of the form submission endpoint
    url = "https://atlas-myrmv.massdot.state.ma.us/myrmv/"

    # Headers (including necessary cookies and other headers)
    headers = {

        "Host": "atlas-myrmv.massdot.state.ma.us",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:128.0) Gecko/20100101 Firefox/128.0",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Content-Type": "application/x-www-form-urlencoded",
        "Fast-Browser-Url": "https://atlas-myrmv.massdot.state.ma.us/myrmv/_/#1",
        "X-Requested-With": "XMLHttpRequest",
        "Content-Length": "473",
        "Origin": "https://atlas-myrmv.massdot.state.ma.us",
        "Connection": "keep-alive",
        "Referer": "https://atlas-myrmv.massdot.state.ma.us/myrmv/_/",
        "Cookie": "tap-bi=eRFDoIKScLqD2kkwTLtibTIeG+i/NDAaO626b89pUGN/Pa70nldZFIELKTQYD9FGxs4HVzhInb1J8kmTQ9xeiuYFSRRDULAqRDE8ZNnALQINcYfv54tMnokC8+fAoOZ3EUFoIyfJA/9oM5BqVLCXpg__; tap-persist=C1hQ1fbxoY9qrVhoYiC3oHtQdN0JfN2uQ3RsTYyBaAgiRkFTVAIAARAA0wig5+Bz3lVU6o4Ed7Pxpw8/Janmw1tYzIbTzMo9jJX/ag6s6bKJ1wEs/ZieMidsxBxmjajxrdCiq1/6CnsQZFyiJGwmN0D51K0GbblIM7c_; wlb-tap-token=GesJDtdanrJuP3aUYj/XVA__; tap-session=C8DYf1DdWfLej5iylqHhQYSO1oQMjifCcUh3Loeo/E9rRkFTVAIAARAAeAllHk29hHL77Xbdvtv+ZmeH69s21IWhIuk6IJFHFIl9TOaPrberSUb5mcr8Wc3jdzG1jzkhUpR/UkmpIqdYLTv4B/o6H3c2f1UNWvGIMerZEUjs7nI1wBPNqJ6EWPuFGqjq0fZDyw6wEBTNXuc8x/XeMJnPp8FqxaOnDg4VK8cOdUi6PtsaTEG0x1o4SdibuOxbmKCQvwUm+ttBzv8D/kVy5zXS4HJ9sm5xCBqn+B5J3pql/Mu2k1e3AfrW4dUA/UGbFKbo1r1t4RdQ6XDCHO56N9TazvvhxRlccDUXolV1uWuGsjqLmIxSn32Nvgfzmgircd5kTpDN0XjHw6EAvw__; _ga=GA1.3.949740451.1710764912; _ga_37BJEZQN1V=GS1.3.1710764912.1.0.1710764912.0.0.0; _ga_B90K4HEWB4=GS1.1.1721477850.10.0.1721477850.0.0.0; _ga_E8VV9Q5Q46=GS1.1.1720956843.3.0.1720956843.0.0.0; _gid=GA1.3.1838975984.1721477851; _gat_gtag_UA_124067955_1=1",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        # Include other headers like User-Agent, cookies, etc. if needed
    }

    s = requests.Session()

    cat = s.get('https://atlas-myrmv.massdot.state.ma.us/myrmv/_/', headers=headers)

    print(requests.get("https://atlas-myrmv.massdot.state.ma.us/myrmv/_/",).text)

    print(cat.text)

    # Data to be sent in the form submission (e.g., license plate information)
    #data = uncurl.parse(
    #    'curl "https://atlas-myrmv.massdot.state.ma.us/myrmv/_/EventOccurred" --compressed -X POST -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:128.0) Gecko/20100101 Firefox/128.0" -H "Accept: application/json, text/javascript, */*; q=0.01" -H "Accept-Language: en-US,en;q=0.5" -H "Accept-Encoding: gzip, deflate, br, zstd" -H "Content-Type: application/x-www-form-urlencoded" -H "Fast-Browser-Url: https://atlas-myrmv.massdot.state.ma.us/myrmv/_/^#5" -H "X-Requested-With: XMLHttpRequest" -H "Origin: https://atlas-myrmv.massdot.state.ma.us" -H "Connection: keep-alive" -H "Referer: https://atlas-myrmv.massdot.state.ma.us/myrmv/_/" -H "Cookie: tap-bi=eRFDoIKScLqD2kkwTLtibTIeG+i/NDAaO626b89pUGN/Pa70nldZFIELKTQYD9FGxs4HVzhInb1J8kmTQ9xeiuYFSRRDULAqRDE8ZNnALQINcYfv54tMnokC8+fAoOZ3EUFoIyfJA/9oM5BqVLCXpg__; tap-persist=C1hQ1fbxoY9qrVhoYiC3oHtQdN0JfN2uQ3RsTYyBaAgiRkFTVAIAARAA0wig5+Bz3lVU6o4Ed7Pxpw8/Janmw1tYzIbTzMo9jJX/ag6s6bKJ1wEs/ZieMidsxBxmjajxrdCiq1/6CnsQZFyiJGwmN0D51K0GbblIM7c_; wlb-tap-token=cneuIyyO8hCSQHybUtVmSA__; tap-session=C3D9oTzi8OktNqh6ovOZUxeeNfpqs5B3Nd+7cgLPdEMaRkFTVAIAARAACvodu2YZQoNPEXDqV9EYo8dyxFqwblvdYr/FOFtYEIaiEKh4yeOVyHSFoJgMV7xwAWeNPJDWDG2SACYKvDCKHQSm0GMbF1XKE2/Pk+8QHUArR9D7/d8nIJST1yqAIpNAzmC2CsC/08Ais0jBwrexOc0oZmQ69uy3oklsObGt9Y8dRGhWWpQEjTArX6ZRX34sJ/in2DSQQB3Ci5kE5FHG/vxFacI6r0yL7K1BKj/et6qFkdHo4kNxAur7s91QPfLNGmK/Pz98jpM0HM6MSdfnEZ81RUtq48cz1ViEX00JeKWMv3gzW6n1/RB5ScZvZKVcDuMU11FYLVaRs2AzwnICTQ__; _ga=GA1.3.949740451.1710764912; _ga_37BJEZQN1V=GS1.3.1710764912.1.0.1710764912.0.0.0; _ga_B90K4HEWB4=GS1.1.1721308123.7.0.1721308123.0.0.0; _ga_E8VV9Q5Q46=GS1.1.1720956843.3.0.1720956843.0.0.0; _gid=GA1.3.2034723858.1721297909" -H "Sec-Fetch-Dest: empty" -H "Sec-Fetch-Mode: cors" -H "Sec-Fetch-Site: same-origin" -H "Priority: u=0" --data-raw "Dd-6=1NDJ16&Dd-7=PAN&Dd-8=PANPL&LASTFOCUSFIELD__=Dd-9&DOC_MODAL_ID__=0&EVENT__=Dd-9&TYPE__=0&CLOSECONFIRMED__=false&SCREENWIDTH__=3&FAST_SCRIPT_VER__=1&FAST_VERLAST__=10.PCI4NBO5._._.PXxW1xhiDNJdN3PUasiSIHelEbg1&FAST_VERLAST_SOURCE__=_^%^3ASetProperties^%^3A2135077096^%^20^%^40^%^202024-07-18^%^2009^%^3A26^%^3A21.1311&FAST_CLIENT_WHEN__=1721309188118&FAST_CLIENT_WINDOW__=FWDC.WND-8e40-104a-866d&FAST_CLIENT_AJAX_ID__=11&FAST_CLIENT_TRIGGER__=DocFieldLinkClick&FAST_CLIENT_SOURCE_ID__=Dd-9"')
    #print(data)
    #session = requests.Session()
    #r = session.get(url, timeout=30, headers=headers, data="Dd-6=1NDJ16&Dd-7=PAN&Dd-8=PANPL&LASTFOCUSFIELD__=Dd-9&DOC_MODAL_ID__=0&EVENT__=Dd-9&TYPE__=0&CLOSECONFIRMED__=false&SCREENWIDTH__=3&FAST_SCRIPT_VER__=1&FAST_VERLAST__=9.IFRUTBW5._._.nF4ysHn3Fmb0FKFByeozXxYuY4I1&FAST_VERLAST_SOURCE__=_%3ARecalc%3A540991543%20%40%202024-07-20%2009%3A17%3A25.2544&FAST_CLIENT_WHEN__=1721481449197&FAST_CLIENT_WINDOW__=FWDC.WND-57cf-d7d0-cdcb&FAST_CLIENT_AJAX_ID__=9&FAST_CLIENT_TRIGGER__=DocFieldLinkClick&FAST_CLIENT_SOURCE_ID__=Dd-9")
#
    #print(r.status_code)

    #response = requests.post(url, headers=headers, data='Dd-6=1NDJ16&Dd-7=PAN&Dd-8=PANPL&LASTFOCUSFIELD__=Dd-9&DOC_MODAL_ID__=0&EVENT__=Dd-9&TYPE__=0&CLOSECONFIRMED__=false&SCREENWIDTH__=3&FAST_SCRIPT_VER__=1&FAST_VERLAST__=10.PCI4NBO5._._.PXxW1xhiDNJdN3PUasiSIHelEbg1&FAST_VERLAST_SOURCE__=_^%^3ASetProperties^%^3A2135077096^%^20^%^40^%^202024-07-18^%^2009^%^3A26^%^3A21.1311&FAST_CLIENT_WHEN__=1721309188118&FAST_CLIENT_WINDOW__=FWDC.WND-8e40-104a-866d&FAST_CLIENT_AJAX_ID__=11&FAST_CLIENT_TRIGGER__=DocFieldLinkClick&FAST_CLIENT_SOURCE_ID__=Dd-9')
    ##Check the response
    #print("Status Code:", response.status_code)
    #print("Response Text:", response.text)


#lookup_registration_info()


class Database_Modifier:
    def __init__(self):
        self.database_name = "Information.db"

    def check_If_Table_Exists(self, table_name, list_of_columns):
        db = sqlite3.connect(self.database_name)

        list_of_columns = [column.replace(" ", "_").replace("-", "_") for column in list_of_columns]
        print(list_of_columns)

        print(table_name + " IS THE TABLE NAME")
        print(
            f"CREATE TABLE IF NOT EXISTS {table_name} (id INTEGER PRIMARY KEY AUTOINCREMENT  , {', '.join([f'{col} TEXT' for col in list_of_columns])})"
        )

        create_table_sql = f"CREATE TABLE IF NOT EXISTS {table_name} (id INTEGER PRIMARY KEY AUTOINCREMENT, {', '.join([f'{col} TEXT' for col in list_of_columns])})"

        db.execute(create_table_sql)
        db.commit()

    def create_Database_Row(self, table_name, dict_of_values):
        db = sqlite3.connect(self.database_name)

        columns = [column_name.replace(" ", "_").replace("-", "_") for column_name in dict_of_values.keys()]
        values = [value.replace(" ", "_").replace("-", "_") for value in dict_of_values.values()]

        print("Values: ")
        for i in values:
            print(i)

        insert_sql = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({', '.join(['?'] * len(columns))})"

        db.execute(insert_sql, values)
        db.commit()

    def read_Database_Single_Table(self, table_name):
        import sqlite3
        import pandas as pd

        sqliteConnection = sqlite3.connect(self.database_name)

        df = pd.read_sql_query("SELECT * FROM " + table_name, sqliteConnection)

        return df

    def read_Database_All_Tables(self, case_number):
        import sqlite3
        import pandas as pd

        try:

            # Making a connection between sqlite3
            # database and Python Program
            sqliteConnection = sqlite3.connect(self.database_name)

            # If sqlite3 makes a connection with python
            # program then it will print "Connected to SQLite"
            # Otherwise it will show errors
            print("Connected to SQLite")

            # Getting all tables from sqlite_master
            sql_query = """SELECT name FROM sqlite_master
            WHERE type='table';"""

            # Creating cursor object using connection object
            cursor = sqliteConnection.cursor()

            # executing our sql query
            list_of_table_names = [table_name[0] for table_name in cursor.execute(sql_query).fetchall()]

            return_dict = {case_number: {}}

            for database_table in list_of_table_names:
                df = pd.read_sql('SELECT * FROM ' + database_table, sqliteConnection)

                if str(database_table) != "sqlite_sequence":
                    return_dict[case_number][database_table] = {}
                print("Table Name: " + str(database_table))

                for index, row in df.iterrows():
                    print("Row : " + str(row.get(key="Case_Number")))
                    if row.get(key="Case_Number") == case_number:

                        return_dict[case_number][database_table][
                            str(row["Basic_Details_First_Name"] + " " + row["Basic_Details_Last_Name"])] = {}
                        for data_name, data_value in row.items():
                            return_dict[case_number][database_table][
                                str(row["Basic_Details_First_Name"] + " " + row["Basic_Details_Last_Name"])][
                                str(data_name)] = str(data_value)

        except AttributeError as error:
            print("Failed to execute the above query", error)

        finally:
            # Inside Finally Block, If connection is
            # open, we need to close it
            if sqliteConnection:
                # using close() method, we will close
                # the connection
                sqliteConnection.close()

                # After closing connection object, we
                # will print "the sqlite connection is
                # closed"
                print("the sqlite connection is closed")
                return return_dict

    def read_Database_Specific_Rows_Names(self, information_tuple):
        import sqlite3
        import pandas as pd

        sqliteConnection = sqlite3.connect(self.database_name)

        print(information_tuple[0])
        print(information_tuple[1])

        exact_match = pd.read_sql(
            "SELECT * FROM People_Of_Interest WHERE Basic_Details_Last_Name =  ? AND Basic_Details_First_Name = ?",
            sqliteConnection, params=information_tuple)

        # if len(exact_match) > 0:

        print(exact_match)
        print(len(exact_match))

        # exact_match = sqliteConnection.execute(
        #    "SELECT * FROM People_Of_Interest WHERE Basic_Details_Last_Name = ? AND Basic_Details_First_Name = ?",
        #    information_tuple)
        #
        # print(exact_match)
        #
        # results = exact_match.fetchall()
        # print(len(results))
        #
        # print(exact_match)

        # CASE WHEN REGEXP_REPLACE(us_1.mls0_PrimaryString, '[[:space:]]') IS NULL THEN ..

        return exact_match

    def update_Database_Table(self):
        pass

    def destroy_Database_Row(self, table_name, id_number):
        db = sqlite3.connect(self.database_name)

        insert_sql = f"DELETE FROM {table_name} WHERE id = '{id_number}'"

        db.execute(insert_sql)
        db.commit()


