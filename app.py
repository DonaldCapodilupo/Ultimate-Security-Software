from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)




@app.route('/', methods=["POST", "GET"])
def main_Menu():
    if request.method == "POST":

        button_clicked = request.form['submit_button']

        if button_clicked == "Submit BOLO":
            print(request.form)
            return render_template("BOLO File.html")
    else:
        return render_template("main.html", list_of_customers=["McDonald's Corp", "Mark 1", "Town of Disney Land",
                                                                   "Snapshot Financials", "Online Giveaway Solutions"])



@app.route('/BOLO-Create', methods=["POST", "GET"])
def create_BOLO():
    if request.method == "POST":


        button_clicked = request.form['submit_button']

        if button_clicked == "Submit BOLO":
            print(request.form)
            return render_template("BOLO File.html")
    else:
        return render_template("BOLO File.html", data={
            "Incident Number": "TOB01-POLCUR-001",
            "Name": "Donald Capodilupo",
            "Alias": "Don, CJ",
            "DOB": "01/01/1990"
        })


@app.route('/Create-New-Case', methods=["POST", "GET"])
def create_New_Case():
    if request.method == "POST":

        button_clicked = request.form['submit_button']

        if button_clicked == "Submit BOLO":
            print(request.form)
            return render_template("BOLO File.html")
    else:
        return render_template("New Case.html", list_of_customers=["McDonald's Corp", "Mark 1", "Town of Billerica",
                                                                   "Snapshot Financials", "Online Giveaway Solutions"])


if __name__ == '__main__':
    app.run()
