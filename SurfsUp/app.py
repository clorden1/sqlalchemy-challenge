# Import the dependencies.
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

import datetime as dt

# #################################################
# # Database Setup
# #################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save reference to the table
meas = Base.classes.measurement
stat = Base.classes.station

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
        f"/api/v1.0/precipitation<br/>"
        f"All precipitation measurements in the last year of data.<br/><br/>"
        f"/api/v1.0/stations<br/>"
        f"All unique station id's.<br/><br/>"
        f"/api/v1.0/tobs<br/>"
        f"All temperature observations from the most active station, USC00519281, in the last year.<br/><br/>"
        f"/api/v1.0/start_date<br/>"
        f"User specified start date. Will return the min, max, and avg temperature for all dates<br/> after specified start date. Date format should be YYYY-MM-DD.<br/><br/>"
        f"/api/v1.0/start_date/end_date<br/>"
        f"User specified start and end date. Will return the min, max, and avg temperature for all<br/> dates between specified start and end dates. Date format should be YYYY-MM-DD.<br/><br/>"
    )

#specify route for precipitation analysis results
@app.route("/api/v1.0/precipitation")
def precipitation():

    #define last year of data
    query_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    #query data
    results = session.query(meas.date, meas.prcp).\
        filter(meas.date >= query_date).all()

    session.close()

    #create a list of dictionaries with results
    all_prcp = []
    for date, prcp in results:
        prcp_dict = {}
        prcp_dict[date] = prcp
        all_prcp.append(prcp_dict)

    #return the list of dictionaries
    return jsonify(all_prcp)

#define route to display all unique stations id's
@app.route("/api/v1.0/stations")
def stations():

    #query the data
    results = session.query(meas.station).distinct().all()

    session.close()

    #create a list of dictionaries and add results to that list
    all_stations = []
    for station in results:
        station_dict = {}
        station_dict["Station ID"] = station[0]
        all_stations.append(station_dict)
    
    #return list of station id's
    return jsonify(all_stations)

#define route for last year of temperature observations
@app.route("/api/v1.0/tobs")
def tobs():
    
    #define last year of date
    query_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    #query data
    results = session.query(meas.date, meas.tobs).\
        filter(meas.date >= query_date, meas.station == "USC00519281").all()
    
    session.close()
    
    #create list of dictionaries and add results to that list
    all_tobs = []
    for date, tobs in results:
        tobs_dict = {}
        tobs_dict[date] = tobs
        all_tobs.append(tobs_dict)
    
    #return list of temperatures
    return jsonify(all_tobs)

#define route for returning temperature data description from specified start date
@app.route("/api/v1.0/<start>")
def start(start):

    #take user inputed start date and ensure it is correct date format
    raw_date = start.replace(" ", "").lower()
    date_format = '%Y-%m-%d'
    query_date = dt.datetime.strptime(raw_date, date_format) # Reference 1

    #query data
    results = session.query(meas.date, func.min(meas.tobs), func.max(meas.tobs), func.avg(meas.tobs)).group_by(meas.date).\
        filter(meas.date >= query_date).all()
    
    session.close()

    #create list of dictionaries with results
    all_tobs = []
    for date, min, max, avg in results:
        tobs_dict = {}
        tobs_dict["date"] = date
        tobs_dict["min temp"] = min
        tobs_dict["max temp"] = max
        tobs_dict["avg temp"] = avg
        all_tobs.append(tobs_dict)
    
    #return list of dictionaries
    return jsonify(all_tobs)

#define route for returning temperature data description between specified start and end date
@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    
    #take user inputed start and end date and ensure it is correct date format
    raw_start = start.replace(" ", "").lower()
    raw_end = end.replace(" ", "").lower()
    date_format = '%Y-%m-%d'
    query_start = dt.datetime.strptime(raw_start, date_format)
    query_end = dt.datetime.strptime(raw_end, date_format)

    #query data
    results = session.query(meas.date, func.min(meas.tobs), func.max(meas.tobs), func.avg(meas.tobs)).group_by(meas.date).\
        filter(meas.date >= query_start, meas.date <= query_end).all()

    session.close()

    #create list of dictionaries with results
    all_tobs = []
    for date, min, max, avg in results:
        tobs_dict = {}
        tobs_dict["date"] = date
        tobs_dict["min temp"] = min
        tobs_dict["max temp"] = max
        tobs_dict["avg temp"] = avg
        all_tobs.append(tobs_dict)

    #return list of dictionaries
    return jsonify(all_tobs)   

#run program from terminal
if __name__ == "__main__":
    app.run(debug=True)