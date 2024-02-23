# Import the dependencies.
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

import datetime as dt

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save reference to the table
meas = Base.classes.measurement
stat = Base.classes.stations

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)



#################################################
# Flask Routes
#################################################

#Home Page
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    results = session.query(meas.date, meas.prcp).all()

    session.close()

    all_prcp = []
    for date, prcp in results:
        prcp_dict = {}
        prcp_dict[date] = prcp
        all_prcp.append(prcp_dict)

    return jsonify(all_prcp)

@app.route("/api/v1.0/stations")
def stations():
    results = session.query(meas.station).distinct().all()

    session.close()

    all_stations = []
    for station in results:
        all_stations.append(station)
    
    return jsonify(all_stations)

@app.tobs("/api/v1.0/tobs")
def tobs():
    query_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    results = session.query(meas.date, meas.tobs).\
        filter(meas.date >= query_date, meas.station == "USC00519281")
    
    session.close()
    
    all_tobs = []
    for tobs in results:
        all_tobs.append(tobs)
    
    return jsonify(all_tobs)

# @app.start("/api/v1.0/<start>")
# def start(start):

# @app.start_end("/api/v1.0/<start>/<end")
# def start_end(start):