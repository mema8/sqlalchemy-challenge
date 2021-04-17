import numpy as np
import pandas as pd
import datetime as dt
from flask import Flask, jsonify

# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

# create engine to hawaii.sqlite
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)


# Save references to each table
Station = Base.classes.station
Measurement = Base.classes.measurement 

# Create our session (link) from Python to the DB
session = Session(engine)
app = Flask(__name__)

@app.route("/")
def hawaii():
    return (
        f"Hello everybody<br>"
        f"/api/v1.0/precipitation<br>"
        f"/api/v1.0/stations<br>"
        f"/api/v1.0/tobs<br>"
        f"/api/v1.0/<start><br>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    last_year = dt.date(2017,8,23) - dt.timedelta(days=365)

    # Perform a query to retrieve the data and precipitation scores
    prcp_results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= last_year).\
                    order_by(Measurement.date).all()
    
    prcp_dict = {date: prcp for date, prcp in prcp_results}
    return jsonify(prcp_dict)

@app.route("/api/v1.0/stations")
def station():
    total_stations = session.query(Station.station).all()
    stations_list = list(np.ravel(total_stations))
    return jsonify(stations_list)

@app.route("/api/v1.0/tobs")
def most_active():
    last_year = dt.date(2017,8,23) - dt.timedelta(days=365)
    temp_most_active = session.query(Measurement.date, Measurement.tobs).\
                        filter(Measurement.station == 'USC00519281').filter(Measurement.date >= last_year).all() 
    temp_list = list(np.ravel(temp_most_active))
    return jsonify(temp_list)

@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def most_less(start=None, end=None):
    if not end:
        temp = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).\
            filter(Measurement.date >= start).all() 
        temp__list = list(np.ravel(temp))
        return jsonify(temp__list)
    temp = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).\
            filter(Measurement.date >= start).filter(Measurement.date <= end).all() 
    temp__list = list(np.ravel(temp))
    return jsonify(temp__list)

if __name__ == '__main__':
    app.run()





