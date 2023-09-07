from flask import Flask, request
from flask_restx import Api
from flask_cors import CORS
import mariadb
from datetime import datetime, timedelta

app = Flask(__name__)
CORS(app, origins='http://localhost:7702')
api = Api(app=app, doc="/docs", title="API Weather", description="API to retrieve weather data", default="API Weather",
          default_label='Weather API', validate=True)

# connection info
host = "localhost"
user = "root"
password = "root"
database = "weather"

# establish connection
conn = mariadb.connect(
    host=host,
    user=user,
    password=password,
    database=database
)

# open the connection
db = conn.cursor()


@app.route("/temperaturesAndHumidity", methods=['GET'])
def temperatures_and_humidity():
    db.execute("SELECT Date, Temperature, Humidity FROM statement ")
    db_temp = db.fetchall()
    temperatures = []

    for temperature in db_temp:
        temperatures.append(
            {"date": temperature[0].strftime("%H:%M"), "temperature": temperature[1], "humidity": temperature[2]})

    return temperatures


@app.route("/hourlyStatements", methods=['GET'])
def hourly():
    db.execute("SELECT Date, Temperature, Humidity FROM statement ORDER BY `Date` ASC")
    db_temp = db.fetchall()
    temperatures = []
    now = datetime.today()

    for temperature in db_temp:
        differ = now - temperature[0]

        if differ < timedelta(hours=1):
            temperatures.append(
                {"date": temperature[0].strftime("%H:%M"), "temperature": temperature[1], "humidity": temperature[2]})

    return temperatures


@app.route("/dailyStatements", methods=['GET'])
def daily():
    db.execute("SELECT Date, Temperature, Humidity FROM statement ORDER BY `Date` ASC")
    db_temp = db.fetchall()
    temperatures = []
    now = datetime.today()

    for temperature in db_temp:
        if now.day == temperature[0].day:
            temperatures.append(
                {"date": temperature[0].strftime("%H:%M"), "temperature": temperature[1], "humidity": temperature[2]})

    return temperatures


@app.route("/addData", methods=['POST'])
def add_data():
    data = request.get_json()

    # insert the temperature and humidity in database
    db.execute(
        f"INSERT INTO statement (`Date`, `Temperature`, `Humidity`) VALUES ('{datetime.today()}', '{data['temperature']}', '{data['humidity']}')")

    # save in database
    conn.commit()

    return {"message": "Informations ajoutées en base de données"}, 200
