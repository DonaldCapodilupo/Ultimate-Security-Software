from flask import Flask, render_template, request, redirect, url_for
from markupsafe import escape



app = Flask(__name__)




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
            "Create BOLO":"create_BOLO",

        }

        reports_that_require_case_numbers = ["Daily Activity Report", "Check Case Status", "Witness Statement",
                                             "Person of Interest",
                                             "Interview Report", "Create BOLO"]

        if button_clicked in reports_that_require_case_numbers:
            return redirect(url_for(redirect_dict[button_clicked], case_number=case_number))
        else:
            return redirect(url_for(redirect_dict[button_clicked]))

    else:
        return render_template("main.html" )


@app.route('/BOLO-Create/<string:case_number>', methods=["POST", "GET"])
def create_BOLO(case_number):
    if request.method == "POST":

        button_clicked = request.form['submit_button']

        if button_clicked == "Submit BOLO":
            from Backend import HTML_To_Database
            data_dict = request.form.to_dict()

            HTML_To_Database("BOLOs", data_dict)


            return redirect(url_for(main_Menu))
    else:

        return render_template("BOLO File.html", case_num=escape(case_number))


@app.route('/Create-New-Case', methods=["POST", "GET"])
def create_New_Case():
    if request.method == "POST":

        button_clicked = request.form['submit_button']


        if button_clicked == "Submit New Case":

            from Backend import HTML_To_Database, create_Case
            data_dict = request.form.to_dict()

            HTML_To_Database("Cases", data_dict)
            create_Case(data_dict["Case Number"])

            
            return redirect(url_for("main_Menu"))
    else:
        return render_template("New Case.html")


@app.route('/Initial-Customer-Report', methods=["POST", "GET"])
def create_Initial_Customer_Report():
    if request.method == "POST":
        from Backend import HTML_To_Database
        data_dict = request.form.to_dict()

        HTML_To_Database("Intital Customer Report", data_dict)
        return redirect(url_for(main_Menu))

    else:
        return render_template("Initial Report.html")


@app.route('/Invoice', methods=["POST", "GET"])
def create_Customer_Invoice():
    if request.method == "POST":
        pass

    else:
        return "Coming Soon!"


@app.route('/Check-Case-Status/<string:case_number>', methods=["POST", "GET"])
def read_Case_Status(case_number):
    if request.method == "POST":
        pass

    else:
        return "Coming Soon!"


@app.route('/Daily-Activity-Report/<string:case_number>', methods=["POST", "GET"])
def create_Daily_Activity_Report(case_number):
    if request.method == "POST":
        from Backend import HTML_To_Database
        data_dict = request.form.to_dict()

        HTML_To_Database("Daily Activity Reports", data_dict)
        return redirect(url_for(main_Menu))

    else:
        return render_template("Daily Activity Report.html", case_num=case_number)


@app.route('/Create-Interview-Report/<string:case_number>', methods=["POST", "GET"])
def create_Interview_Report(case_number):
    if request.method == "POST":
        pass

    else:
        return render_template("Interview Report.html", case_num=case_number)


@app.route('/Create-Person-Of-Interest-Report/<string:case_number>', methods=["POST", "GET"])
def create_Person_Of_Interest_Report(case_number):
    if request.method == "POST":
        pass

    else:
        return render_template("Person of Interest.html", case_num=case_number)


@app.route('/Create-Witness-Statement-Report/<string:case_number>', methods=["POST", "GET"])
def create_Witness_Statement_Report(case_number):
    if request.method == "POST":
        pass

    else:
        return render_template("Witness Statement Form.html", case_num=case_number)


if __name__ == '__main__':
    app.run()
