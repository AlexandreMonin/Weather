import pdb

from flask import Flask, request
from flask_restx import Api, Resource, fields
from flask_cors import CORS
import mariadb
from datetime import datetime, timedelta

app = Flask(__name__)
CORS(app, origins='http://localhost:7702')
api = Api(app=app, doc="/api")

statement = api.model('statement', {
    'temperature': fields.Float(required=True),
    'humidity': fields.Float(required=True)
})
sonde = api.model('sonde', {
    'name': fields.String(required=True),
    'longitude': fields.Float(required=True),
    'latitude': fields.Float(required=True)
})

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


@api.route("/getAll", methods=['GET'])
class getAll(Resource):
    def get(self):
        db.execute("SELECT Date, Temperature, Humidity FROM statement ")
        db_temp = db.fetchall()
        temperatures = []

        for temperature in db_temp:
            temperatures.append(
                {"date": temperature[0].strftime("%H:%M"), "temperature": temperature[1], "humidity": temperature[2]})

        return temperatures


@api.route("/hourlyStatements", methods=['GET'])
class hourlyStatements(Resource):
    def get(self):
        db.execute("SELECT Date, Temperature, Humidity FROM statement ORDER BY `Date` ASC")
        db_temp = db.fetchall()
        temperatures = []
        now = datetime.today()

        for temperature in db_temp:
            differ = now - temperature[0]

            if differ < timedelta(hours=1):
                temperatures.append(
                    {"date": temperature[0].strftime("%H:%M"), "temperature": temperature[1],
                     "humidity": temperature[2]})

        return temperatures


@api.route("/dailyStatements", methods=['GET'])
class dailyStatements(Resource):

    def get(self):
        db.execute("SELECT Date, Temperature, Humidity FROM statement ORDER BY `Date` ASC")
        db_temp = db.fetchall()
        temperatures = []
        now = datetime.today()

        for temperature in db_temp:
            if now.day == temperature[0].day:
                temperatures.append(
                    {"date": temperature[0].strftime("%H:%M"), "temperature": temperature[1],
                     "humidity": temperature[2]})

        return temperatures


@api.route("/addData", methods=['POST'])
@api.expect(statement)
class addData(Resource):
    def post(self):
        datas = request.get_json()

        db.execute("SELECT Id FROM sonde")
        sonde_ids = db.fetchall()

        for data in range(len(datas['temperature'])):
            db.execute(
                 f"INSERT INTO statement (`Date`, `Temperature`, `Humidity`, `SondeId`) VALUES ('{datetime.today()}', '{datas['temperature'][data]}', '{datas['humidity'][data]}', {sonde_ids[data][0]})")

        # save in database
        conn.commit()

        db.execute(
            "SELECT COUNT(*) AS row_account FROM sonde;"
        )

        account = db.fetchall()

        return account[0][0], 200


@api.route("/addSonde", methods=['POST'])
@api.expect(sonde)
class addSonde(Resource):

    def post(self):
        data = request.get_json()

        # insert the temperature and humidity in database
        db.execute(
            f"INSERT INTO sonde (`Name`, `Longitude`, `Latitude`) VALUES ('{data['name']}', '{data['longitude']}', '{data['latitude']}')")

        # save in database
        conn.commit()

        return {"message": "Informations ajoutées en base de données"}, 200
