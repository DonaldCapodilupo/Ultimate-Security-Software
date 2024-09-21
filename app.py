from flask import Flask, render_template, request, redirect, url_for
from markupsafe import escape
from flask_nav import Nav
from flask_nav.elements import Navbar, View
import serial



try:
    ser = serial.Serial('COM3', 9600)
    serial_port_found = True
except serial.serialutil.SerialException:
    serial_port_found = False


app = Flask(__name__)
nav = Nav()


# Generic Functions
@app.route('/', methods=["POST", "GET"])
def main_Menu():
    if request.method == "POST":
        button_clicked = request.form['submit_button']
        # case_number = request.form['Case Number']
        redirect_dict = {
            "New Customer Report": "create_Initial_Customer_Report",
            "Create New Case": "create_New_Case",
            "Create Invoice": "create_Customer_Invoice",
            "Check Case Status": "read_Case_Status",
            "Daily Activity Report": "create_Daily_Activity_Report",
            "Interview Report": "create_Interview_Report",
            "Person of Interest": "create_Person_Of_Interest_Report",
            "Witness Statement": "create_Witness_Statement_Report",
            "Create BOLO": "create_BOLO",
            "Capture Plate": "capture_Plate_Image",
            "Search Database": "search_Database"
        }

        reports_that_require_case_numbers = ["Daily Activity Report", "Check Case Status", "Witness Statement",
                                             "Person of Interest",
                                             "Interview Report", "Create BOLO"]
        return redirect(url_for(redirect_dict[button_clicked]))

        # if button_clicked in reports_that_require_case_numbers:
        #    return redirect(url_for(redirect_dict[button_clicked], case_number=case_number))
        # else:


    else:
        from Backend import Database_Modifier

        backend_data = Database_Modifier().read_Database_Single_Table("New_Case")
        case_numbers = backend_data["Case_Number"].to_list()

        data_dict = {
            "Case Number": [case_number.replace("_", "-") for case_number in case_numbers]
        }

        if len(request.args) >= 1:
            confirmation = request.args["confirmation"]
        else:
            confirmation = ""

        print(serial_port_found)
        return render_template("main.html", infoDict=data_dict, confirmation=confirmation, serial_port_found=serial_port_found)


@app.route('/Check-Case-Status/<string:case_number>', methods=["POST", "GET"])
def read_Case_Status(case_number):
    if request.method == "POST":
        pass

    else:
        from Backend import Database_Modifier

        # Right now, just pulling one specific user for proof of concept.
        # Need a way to go "Okay user wants this case number" then search all tables for anything related.

        case_reports = Database_Modifier().read_Database_Single_Table("New_Case")

        col_headers = [col for col in case_reports.columns]
        print(col_headers)

        print(case_reports.head())
        specific_case_report = case_reports.loc[case_reports["Case_Number"] == case_number.replace("-", "_")]

        return_Dict_New_Case = {

        }

        # "Customer Name": specific_case_report.Customer_Name.item().replace("_", " "),
        #    "Investigation Type": specific_case_report.Investigation_Type.item().replace("_", " "),
        #    "Case Purpose": specific_case_report.Case_Purpose.item().replace("_", " "),
        #    "Case Scope": specific_case_report.Case_Scope.item().replace("_", " "),

        for header in col_headers:
            if header == "id" or header == "submit_button":
                continue
            else:
                return_Dict_New_Case[header.replace("_", " ")] = specific_case_report[header].item().replace("_", " ")

        customer_first_name = return_Dict_New_Case["Customer Name"].split(" ")[0]
        customer_last_name = return_Dict_New_Case["Customer Name"].split(" ")[1]

        initial_report = Database_Modifier().read_Database_Single_Table("Initial_Customer_Report")

        other_headers = [col for col in initial_report.columns]

        specific_initial_report = initial_report.loc[
            initial_report["Complainant_Last_Name"] == customer_last_name]

        for header in other_headers:
            if header == "id" or header == "submit_button":
                continue
            else:
                return_Dict_New_Case[header.replace("_", " ")] = specific_initial_report[header].item().replace("_",
                                                                                                                " ")

        return render_template("View Data/View Case.html", case_number=case_number, infoDict=return_Dict_New_Case)


# Admin Functions
@app.route('/Initial-Customer-Report', methods=["POST", "GET"])
def create_Initial_Customer_Report():
    if request.method == "POST":
        from Backend import save_Admin_Form_Data, Database_Modifier
        data_dict = request.form.to_dict()

        Database_Modifier().check_If_Table_Exists("Initial_Customer_Report", data_dict.keys())
        Database_Modifier().create_Database_Row("Initial_Customer_Report", data_dict)

        return redirect(url_for("main_Menu"))

    else:
        from Backend import Database_Modifier

        backend_data = Database_Modifier().read_Database_Single_Table("Employees")
        employee_names = backend_data["Name"].to_list()

        data_to_fill = {"Agent Receiving": employee_names,
                        "Case Lead Investigator": employee_names,
                        "Investigating Agent": employee_names,
                        "Manager Reviewing": employee_names,
                        }

        print(employee_names)

        return render_template("Capture Data/Initial Report.html", infoDict=data_to_fill)


@app.route('/Create-New-Case', methods=["POST", "GET"])
def create_New_Case():
    if request.method == "POST":

        from Backend import Database_Modifier, create_Case
        data_dict = request.form.to_dict()

        Database_Modifier().check_If_Table_Exists("New_Case", data_dict.keys())
        Database_Modifier().create_Database_Row("New_Case", data_dict)

        create_Case(data_dict["Case Number"])

        return redirect(url_for("main_Menu"))
    else:
        from Backend import Database_Modifier

        backend_data = Database_Modifier().read_Database_Single_Table("Initial_Customer_Report")
        first_names = backend_data["Complainant_First_Name"].to_list()
        last_names = backend_data["Complainant_Last_Name"].to_list()

        customer_names = []

        for first_nam, last_nam in zip(first_names, last_names):
            customer_names.append(first_nam + " " + last_nam)

        print("Customer Names:")
        print(customer_names)
        data_to_fill = {
            "Customer Name": customer_names
        }

        return render_template("Capture Data/New Case.html", infoDict=data_to_fill)


@app.route('/Invoice', methods=["POST", "GET"])
def create_Customer_Invoice():
    if request.method == "POST":
        pass

    else:
        return "Coming Soon!"


@app.route('/BOLO-Create/', methods=["POST", "GET"])
def create_BOLO():
    if request.method == "POST":
        from Backend import Database_Modifier
        data_dict = request.form.to_dict()

        Database_Modifier("BOLOs").check_If_Table_Exists(data_dict.keys())
        Database_Modifier("BOLOs").create_Database_Row(data_dict)

        return redirect(url_for("main_Menu"))
    else:

        return render_template("Capture Data/BOLO File.html")


# Investigator Functions
@app.route('/Create-Person-Of-Interest-Report/', methods=["POST", "GET"])
def create_Person_Of_Interest_Report():
    if request.method == "POST":
        button_clicked = request.form['submit_button']

        if button_clicked == "Return Home":
            return redirect(url_for("main_Menu"))
        else:
            from Backend import Database_Modifier
            data_dict = request.form.to_dict()

            Database_Modifier().check_If_Table_Exists("People_Of_Interest", data_dict.keys())
            Database_Modifier().create_Database_Row("People_Of_Interest", data_dict)
            return redirect(url_for("main_Menu"))

    else:
        return render_template("Capture Data/Person of Interest.html")


@app.route('/Create-Interview-Report/', methods=["POST", "GET"])
def create_Interview_Report():
    if request.method == "POST":
        from Backend import Database_Modifier
        data_dict = request.form.to_dict()

        Database_Modifier().check_If_Table_Exists("Interview_Reports", data_dict.keys())
        Database_Modifier().create_Database_Row("Interview_Reports", data_dict)
        return redirect(url_for("main_Menu"))

    else:
        return render_template("Capture Data/Interview Report.html")


@app.route('/Create-Witness-Statement-Report', methods=["POST", "GET"])
def create_Witness_Statement_Report():
    if request.method == "POST":
        from Backend import Database_Modifier
        data_dict = request.form.to_dict()

        Database_Modifier().check_If_Table_Exists("Interview_Reports", data_dict.keys())
        Database_Modifier().create_Database_Row("Interview_Reports", data_dict)
        return redirect(url_for("main_Menu"))

    else:
        return render_template("Capture Data/Witness Statement Form.html")


@app.route('/Daily-Activity-Report/', methods=["POST", "GET"])
def create_Daily_Activity_Report():
    if request.method == "POST":
        from Backend import Database_Modifier
        data_dict = request.form.to_dict()

        Database_Modifier().check_If_Table_Exists("Daily_Activity_Reports", data_dict.keys())
        Database_Modifier().create_Database_Row("Daily_Activity_Reports", data_dict)
        return redirect(url_for("main_Menu"))

    else:
        return render_template("Capture Data/Daily Activity Report.html")


@app.route('/House-Profile/', methods=["POST", "GET"])
def read_House_Profile_Report():
    if request.method == "POST":
        pass
    else:
        from Backend import Database_Modifier
        test_dict = {
            "Complainant First Name": "Donald",
            "Complainant Last Name": "Capodilupo",
            "Phone Number": "978/424/5947",
            "Complainant Address": "15 Elizabeth Rd",
            "Complainant Town": "Billerica",
            "Complainant State": "MA",
            "Complainant ZIP": "01821",

        }

        infoDict = Database_Modifier().read_Database_Single_Table("People_Of_Interest").to_dict()
        # est_dict = dict(infoDict[0])

        return render_template("View Data/Non Admin House Profile.html", infoDict=test_dict)


@app.route('/Capture-Plate/', methods=["POST", "GET"])
def capture_Plate_Image():
    from Backend import get_OBS_Zoom
    if request.method == "POST":
        from Backend import license_Plate_Capture
        import os, time
        button_clicked = request.form['submit_button']

        if button_clicked == "Return Home":
            return redirect(url_for("main_Menu"))
        elif button_clicked == "Capture Plate":
            license_Plate_Capture()
            time.sleep(2)
            return render_template("Capture Data/Capture Plate.html", image=True, zoom_level=get_OBS_Zoom())

        elif button_clicked == "Delete Plate":
            print(os.getcwd())
            os.remove("static/images/Screenshot_.png")
            return render_template("Capture Data/Capture Plate.html", image=False, zoom_level=get_OBS_Zoom())

        elif button_clicked == "Update Zoom":
            from Backend import control_OBS_Zoom

            user_desired_zoom = request.form["Updated Zoom Level"]
            control_OBS_Zoom(user_desired_zoom)
            return render_template("Capture Data/Capture Plate.html", image=False, zoom_level=get_OBS_Zoom())

        elif button_clicked == "Save Data":
            import shutil
            from Backend import Database_Modifier

            data_dict = request.form.to_dict()
            print(data_dict)

            Database_Modifier().check_If_Table_Exists("Plate_Captures", data_dict.keys())
            Database_Modifier().create_Database_Row("Plate_Captures", data_dict)

            shutil.move("static/images/Screenshot_.png", "Plates/" + data_dict["License Plate Number"] + ".png")

            return redirect(url_for("main_Menu", confirmation=data_dict["License Plate Number"] + " has been logged."))



        else:

            return render_template("Capture Data/Capture Plate.html")

    else:
        try:
            return render_template("Capture Data/Capture Plate.html", zoom_level=get_OBS_Zoom())
        except ConnectionRefusedError as error:
            print(error)
            return redirect(url_for("main_Menu"))


# Read Data
@app.route('/Search/', methods=["POST", "GET"])
def search_Database():
    if request.method == "POST":
        button_clicked = request.form['submit_button']
        if button_clicked == "Return Home":
            return redirect(url_for("main_Menu"))
        elif button_clicked == "Search Person":
            from Backend import Database_Modifier

            data_dict = request.form.to_dict()
            print(data_dict)

            for value in data_dict.keys():
                if data_dict[value] == "":
                    data_dict[value] = "IGNORE"

            users = Database_Modifier().read_Database_Specific_Rows_Names((data_dict["Basic Details Last Name"],
                                                                           data_dict["Basic Details First Name"]))
            for user in users:
                print(user)

            return redirect(url_for("main_Menu"))

        elif button_clicked == "Search Vehicle":
            data_dict = request.form.to_dict()
            print(data_dict)
            return redirect(url_for("main_Menu"))
        else:
            pass

    else:

        return render_template("View Data/Search.html")


@app.route('/Plate-Lookup/', methods=["POST", "GET"])
def read_Plate_Information():
    from Backend import get_OBS_Zoom
    if request.method == "POST":
        from Backend import license_Plate_Capture
        import os, time
        button_clicked = request.form['submit_button']

        if button_clicked == "Return Home":
            return redirect(url_for("main_Menu"))
        else:
            return render_template("Capture Data/Capture Plate.html")




    else:

        return render_template("View Data/Capture Plate.html", zoom_level=get_OBS_Zoom())


@app.route('/POI/', methods=["POST", "GET"])
def read_POI_Information():
    from Backend import get_OBS_Zoom
    if request.method == "POST":
        from Backend import license_Plate_Capture
        import os, time
        button_clicked = request.form['submit_button']

        if button_clicked == "Return Home":
            return redirect(url_for("main_Menu"))
        else:
            return render_template("View Data/Non Admin Person of Interest Report.html")




    else:
        test_dict = {
            "Complainant First Name": "Donald",
            "Complainant Last Name": "Capodilupo",
            "Phone Number": "978/424/5947",
            "Complainant Address": "15 Elizabeth Rd",
            "Complainant Town": "Billerica",
            "Complainant State": "MA",
            "Complainant ZIP": "01821",

        }

        return render_template("View Data/Non Admin Person of Interest Report.html", infoDict=test_dict)


@app.route('/Map/', methods=["POST", "GET"])
def read_Map():
    from flask import render_template_string
    import plotly.graph_objects as go
    import pandas as pd
    import plotly.express as px

    lat = [19.368894, 19.378639, 19.356536,
           19.352141, 19.376943, 19.351838,
           19.377563, 19.340928, 19.319919,
           19.308241, 19.351663, 19.336423,
           19.350884]

    lon = [-99.005523, -99.107726, -99.101254,
           -99.041698, -99.058977, -99.091929,
           -99.071414, -99.061082, -99.119510,
           -99.066347, -99.010367, -99.050018,
           -98.996826]

    territoriales = ['ACATITLA-ZARAGOZA', 'ACULCO', 'ATLALILCO-AXOMULCO',
                     'AZTAHUACAN', 'CABEZA DE JUAREZ', 'ESTRELLA-HUIZACHEPETL',
                     'LEYES DE REFORMA', 'LOS ANGELES-AGRARISTA', 'LOS CULHUACANES',
                     'SAN LORENZO TEZONCO', 'SANTA CATARINA', 'SANTA CRUZ-QUETZALCOATL',
                     'TEOTONGO-ACAHUALTEPEC']

    dict_map = {'territorial': territoriales, 'lat': lat, 'lon': lon}
    geopd = pd.DataFrame.from_dict(dict_map)
    # print(geopd.head())

    px.set_mapbox_access_token(
        'pk.eyJ1IjoiZ2ZlbGl4IiwiYSI6ImNrZTNsbnYzMTBraG0zMnFuZXNjOWZhdDgifQ.5sMKH7NQ6_oVyU4oJlcBUw')

    fig = px.scatter_mapbox(geopd, lat="lat", lon="lon", zoom=11, width=500, height=300,
                            text="territorial", center={'lat': 19.340928, 'lon': -99.061082})

    fig.update_layout(mapbox_style='outdoors', margin={"r": 0, "t": 0, "l": 0, "b": 0})

    div = fig.to_html(full_html=False)

    return render_template_string('''
    <head>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>    
    </head>
    <body>
    {{ div_placeholder|safe }}
    </body>''', div_placeholder=div)

@app.route('/pattern/<int:pattern_id>')
def set_pattern(pattern_id):
    if ser.is_open:
        ser.write(str(pattern_id-1).encode())
        return f'Pattern {pattern_id + 1} Activated'
    else:
        return 'Serial port not open'

@app.route('/Light-Bar/', methods=["POST", "GET"])
def light_Bar():
    return render_template("Light Bar.html")

if __name__ == '__main__':
    nav.init_app(app)
    app.run(host="0.0.0.0", debug=True, use_reloader=False)
