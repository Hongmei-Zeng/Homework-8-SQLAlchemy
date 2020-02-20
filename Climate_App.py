import os
import sqlalchemy
from sqlalchemy import create_engine, inspect, func
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from flask import Flask, jsonify, request, abort
from datetime import datetime

db_path = os.path.join('Resources', 'hawaii.sqlite')
engine = create_engine(f'sqlite:///{db_path}', connect_args={'check_same_thread': False})

inspector = inspect(engine)
table_names = inspector.get_table_names()

Base = automap_base()
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(bind=engine)

app = Flask(__name__)

@app.route("/")
def home():
    return (
        f"Part2 - Climate_App HomePage<br/>"
        f"<br/>"
        f"Available Routes are: <br/>"
        f"<br/>"
        f"/api/v1.0/precipitation <br/>"
        f"/api/v1.0/stations <br/>"
        f"/api/v1.0/tobs <br/>"
        f"/api/v1.0/vaction <br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    prcp_data = session.query(Measurement.date, Measurement.prcp).all()
    return jsonify(prcp_data)

@app.route("/api/v1.0/stations")
def stations():
    station_ls = session.query(Station.station).all()
    return jsonify(station_ls)

@app.route("/api/v1.0/tobs")
def tobs():
    tobs_12mths = session.query(Measurement.date, Measurement.tobs)\
                    .filter(Measurement.date>'2016-08-23',Measurement.date<='2017-08-23')\
                    .order_by(Measurement.date.asc())\
                    .all()
    return jsonify(tobs_12mths)

def calc_temps(start_date, end_date):
    temp_ls = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs))\
                        .filter(Measurement.date >= start_date)\
                        .filter(Measurement.date <= end_date)\
                        .all()                            
    return temp_ls

@app.route("/api/v1.0/vacation")
def trip():
    request_start_date = request.args['start_date']
    start_date = datetime.strptime(request_start_date, '%Y-%m-%d')

    request_end_date = request.args.get('end_date')
    try:
        if request_end_date:
            end_date = datetime.strptime(request_end_date, '%Y-%m-%d')
        else:
            end_date = session.query(func.max(Measurement.date))     
        return jsonify(calc_temps(start_date, end_date))

    except Exception as e:
        return jsonify({"Status":"Failure!", "Error": str(e)})

if __name__ == "__main__":
    app.run(debug=True)
