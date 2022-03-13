from flask import Flask, redirect, url_for, render_template, request
import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
import datetime as dt

Nombre_velo = 1

scope = ['https://www.googleapis.com/auth/spreadsheets', "https://www.googleapis.com/auth/drive.file",
         "https://www.googleapis.com/auth/drive"]

creds = ServiceAccountCredentials.from_json_keyfile_name('secret_sheet.json', scope)

client = gspread.authorize(creds)

sheet = client.open('SDP_Test').sheet1


def insertion(reservation):
    """
    :param reservation: liste [nom, pnom, date, numvelo, etat_reservation, datetime]
    :return: void
    place la réservation dans le spreasheet sdp
    """
    request_data = sheet.get_all_values()
    LastLineNumber = len(request_data) + 1
    sheet.insert_row(reservation, LastLineNumber)
    sheet.sort((3, 'des'))


#insertion(["alize", "ielsch", "07/03/2022", str(dt.datetime.now())])


def available(date):

    request_data = sheet.get_all_values()
    df = pd.DataFrame(request_data)
    if len(df) == 0 :
        return True
    df.columns = ['Nom', 'Prénom', 'date', 'datetime']
    N = 0
    for i in df.index:
        if df['date'][i] == date :
            N += 1
        if N == Nombre_velo :
            return False
    return True



app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        user_name = request.form["nm"]
        user_pname = request.form["pm"]
        user_date = request.form["dt"]
        if available(user_date) :
            reservation = [str(user_name), str(user_pname), str(user_date), str(dt.datetime.now())]
            insertion(reservation)
            return validation()
        else :
            return invalidation(user_date)
        #return redirect(url_for("check", data="Nom: " + str(user_name) + "\n" + "Prénom: " + str(user_pname) + "\n" + "Date: " + str(user_date)))
    else:
        return render_template("login.html")

# vérifiication des infos
@app.route("/<data>")
def check(data):
    return f"<h1>{'Ces informations sont-elles valides ?'}</h1> <p>{data}</p>"


@app.route("/<validation>")
def validation():
    return f"<h1>Demande de prêt enregistrée</h1>"


@app.route("/<invalidation>")
def invalidation(date):
    return f"<h1>Pas de place pour cette date {date}, essayez une autre date svp</h1>"


if __name__ == "__main__":
    app.run(debug=True)


"""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"""
