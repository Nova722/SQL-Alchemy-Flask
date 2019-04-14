from flask import Flask, jsonify
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import numpy as np
import datetime as dt

## Database Setup
#################################################

engine = create_engine("sqlite:///hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)

app = Flask(__name__)

## Flask Routes
#################################################

@app.route("/")
def welcome():
    return (
        f"<h1>Welcome!<h1><br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end<br/>"
    )


@app.route("/api/v1.0/precipitation")
def precipitiation():
    # Query 
    results = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date > '2010-01-01', Measurement.date < '2015-01-01').order_by(Measurement.date).all()
    all_results = []
    for result in results:
        result_dict = {}
        result_dict["date"] = result.date
        result_dict["prcp"] = result.prcp
        all_results.append(result_dict)

    return jsonify(all_results)


@app.route("/api/v1.0/stations")
def stations():
    results = session.query(Station.station, Station.name).all()
    all_station_results = []
    for result in results:
        result_dict = {}
        result_dict["station_id"] = result.station
        result_dict["station"] = result.name
        all_station_results.append(result_dict)
    return jsonify(all_station_results)


@app.route("/api/v1.0/tobs")
def tobs():
    results = session.query(Measurement.date, Measurement.tobs).\
    filter(Measurement.date.between('2016-08-23','2017-08-23')).order_by(Measurement.date).all()
    all_temp_results = []
    for result in results:
        result_dict = {}
        result_dict["date"] = result.date
        result_dict["temp"] = result.tobs
        all_temp_results.append(result_dict)
    return jsonify(all_temp_results)

if __name__ == '__main__':
    app.run(debug=True)