from flask import Flask, render_template, request, redirect, url_for
from markupsafe import escape

app = Flask(__name__)

#Generic Functions
@app.route('/', methods=["POST", "GET"])
def main_Menu():
    if request.method == "POST":
        button_clicked = request.form['submit_button']
        case_number = request.form['Case Number']
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
        }

        reports_that_require_case_numbers = ["Daily Activity Report", "Check Case Status", "Witness Statement",
                                             "Person of Interest",
                                             "Interview Report", "Create BOLO"]

        if button_clicked in reports_that_require_case_numbers:
            return redirect(url_for(redirect_dict[button_clicked], case_number=case_number))
        else:
            return redirect(url_for(redirect_dict[button_clicked]))

    else:
        from Backend import Database_Modifier

        backend_data = Database_Modifier().read_Database_Single_Table("New_Case")
        case_numbers = backend_data["Case_Number"]

        data_dict = {
            "Case Number":case_numbers
        }

        return render_template("main.html", infoDict=data_dict)

@app.route('/Check-Case-Status/<string:case_number>', methods=["POST", "GET"])
def read_Case_Status(case_number):
    if request.method == "POST":
        pass

    else:
        return "Coming Soon!"


#Admin Functions
@app.route('/Initial-Customer-Report', methods=["POST", "GET"])
def create_Initial_Customer_Report():
    if request.method == "POST":
        from Backend import save_Admin_Form_Data, Database_Modifier
        data_dict = request.form.to_dict()


        Database_Modifier().check_If_Table_Exists("Initial_Customer_Report",data_dict.keys())
        Database_Modifier().create_Database_Row("Initial_Customer_Report",data_dict)



        return redirect(url_for("main_Menu"))

    else:
        from Backend import Database_Modifier

        backend_data = Database_Modifier().read_Database_Single_Table("Employees")
        employee_names = backend_data["Name"].to_list()

        data_to_fill = {"Agent Receiving":employee_names,
                        "Case Lead Investigator": employee_names,
                        "Investigating Agent":employee_names,
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
        Database_Modifier().create_Database_Row("New_Case",data_dict)

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
            "Customer Name":customer_names
        }
        #customer_names = [first_name for first_name in zip(backend_data["Complainant_First_Name"]), backend_data["Complainant_Last_Name"] ]

            #zip(backend_data["Complainant_First_Name"], backend_data["Complainant_Last_Name"])

        #print(customer_names)

        return render_template("Capture Data/New Case.html", infoDict=data_to_fill)

@app.route('/Invoice', methods=["POST", "GET"])
def create_Customer_Invoice():
    if request.method == "POST":
        pass

    else:
        return "Coming Soon!"

@app.route('/BOLO-Create/<string:case_number>', methods=["POST", "GET"])
def create_BOLO(case_number):
    if request.method == "POST":
        from Backend import Database_Modifier
        data_dict = request.form.to_dict()

        Database_Modifier("BOLOs").check_If_Table_Exists(data_dict.keys())
        Database_Modifier("BOLOs").create_Database_Row(data_dict)

        return redirect(url_for("main_Menu"))
    else:

        return render_template("Capture Data/BOLO File.html", case_num=escape(case_number))


#Investigator Functions
@app.route('/Create-Person-Of-Interest-Report/<string:case_number>', methods=["POST", "GET"])
def create_Person_Of_Interest_Report(case_number):
    if request.method == "POST":
        from Backend import Database_Modifier
        data_dict = request.form.to_dict()

        Database_Modifier().check_If_Table_Exists("People_Of_Interest", data_dict.keys())
        Database_Modifier().create_Database_Row("People_Of_Interest", data_dict)
        return redirect(url_for("main_Menu"))

    else:
        return render_template("Capture Data/Person of Interest.html", case_num=case_number)

@app.route('/Create-Interview-Report/<string:case_number>', methods=["POST", "GET"])
def create_Interview_Report(case_number):
    if request.method == "POST":
        from Backend import Database_Modifier
        data_dict = request.form.to_dict()

        Database_Modifier().check_If_Table_Exists("Interview_Reports", data_dict.keys())
        Database_Modifier().create_Database_Row("Interview_Reports", data_dict)
        return redirect(url_for("main_Menu"))

    else:
        return render_template("Capture Data/Interview Report.html", case_num=case_number)

@app.route('/Create-Witness-Statement-Report/<string:case_number>', methods=["POST", "GET"])
def create_Witness_Statement_Report(case_number):
    if request.method == "POST":
        from Backend import Database_Modifier
        data_dict = request.form.to_dict()

        Database_Modifier().check_If_Table_Exists("Interview_Reports", data_dict.keys())
        Database_Modifier().create_Database_Row("Interview_Reports", data_dict)
        return redirect(url_for("main_Menu", case_num=case_number))

    else:
        return render_template("Capture Data/Witness Statement Form.html", case_num=case_number)

@app.route('/Daily-Activity-Report/<string:case_number>', methods=["POST", "GET"])
def create_Daily_Activity_Report(case_number):
    if request.method == "POST":
        from Backend import Database_Modifier
        data_dict = request.form.to_dict()

        Database_Modifier().check_If_Table_Exists("Daily_Activity_Reports", data_dict.keys())
        Database_Modifier().create_Database_Row("Daily_Activity_Reports", data_dict)
        return redirect(url_for("main_Menu"))

    else:
        return render_template("Capture Data/Daily Activity Report.html", case_num=case_number)


if __name__ == '__main__':
    app.run(host="0.0.0.0")
