# Import the dependencies.
import numpy as np
import datetime as dt
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
from sqlalchemy.ext.automap import automap_base

#################################################
# Database Setup
#################################################

# reflect an existing database into a new model
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
measurement = Base.classes.measurement
station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def home():
    print("Home page")
    return (f"Current Routes: <br>"
            f"/ <br>"
            f"/api/v1.0/<start><br>"
            f"/api/v1.0/precipitation<br>"
            f"/api/v1.0/stations<br>"
            f"/api/v1.0/tobs<br>"
            f"/api/v1.0/<start>/<end>")

# create precipitation route
@app.route("/api/v1.0/precipitation")
def precipitation():
    # create the session
    session = Session(bind=engine)
    
    last_date = dt.date(2017,8,23)
    year_before = last_date - dt.timedelta(days=365)

    # query results from precipitation analysis, retrieving only the last 12 months of data
    prcp_result = session.query(measurement.date, 
                            measurement.prcp).\
                            filter(measurement.date >= year_before, measurement.date <= last_date).\
                            filter(measurement.prcp.isnot(None)).\
                            order_by(measurement.date).all()
    
    # make an empty list and store the dictionaries
    prcp_result_list = []
    for result in prcp_result:
        prcp_result_dict = {}
        prcp_result_dict["date"] = result["date"]
        prcp_result_dict["prcp"] = result["prcp"]
        prcp_result_list.append(prcp_result_dict)

    # jsonify and display the contents in the list
    return jsonify(prcp_result_list)

# create stations route
@ app.route("/api/v1.0/stations")
def stations():
    # create the session
    session = Session(bind=engine)

    # query all stations from the dataset
    station_result = session.query(station.station).all()

    # use np.ravel() to turn the tuple into a list
    station_list = list(np.ravel(station_result))

    # jsonify and display the contents in the list
    return jsonify(station_list)

# create temperature observations route
@ app.route("/api/v1.0/tobs")
def tobs():
    # create the session
    session = Session(bind=engine)

    last_date = dt.date(2017,8,23)
    year_before = last_date - dt.timedelta(days=365)

    # query the dates and temperature observations of the most-active station ('USC00519281') for the previous year of data
    tobs_result = session.query(measurement.date, 
                            measurement.tobs).\
                            filter(measurement.date >= year_before, measurement.date <= last_date).\
                            filter(measurement.station == 'USC00519281').\
                            order_by(measurement.date).all()
    
    # make an empty list and store the dictionaries
    tobs_result_list = []
    for result in tobs_result:
        tobs_result_dict = {}
        tobs_result_dict['date'] = result['date']
        tobs_result_dict['tobs'] = result['tobs']
        tobs_result_list.append(tobs_result_dict)

    # jsonify and display the contents in the list
    return jsonify(tobs_result_list)
    
# create the start route
@ app.route("/api/v1.0/<start>")
def start(start):
    # create the session
    session = Session(engine)

    # query temperatures and calculate the minimum, average, and maximum temperature for
    # all the dates greater than or equal to the start date
    start_result = session.query(measurement.tobs,
                                 func.min(measurement.tobs), 
                                 func.max(measurement.tobs), 
                                 func.avg(measurement.tobs)).\
                                 filter(measurement.date >= start).all()

    # make an empty list and store the dictionaries
    temperature_list = []
    for result in start_result:
        start_dict = {}
        start_dict['Minimum Temperature'] = result[1]
        start_dict['Maximum Temperature'] = result[2]
        start_dict['Average Temperature'] = result[3]
        temperature_list.append(start_dict)

    # jsonify and display the contents in the list
    if len(temperature_list) != 0:
        return jsonify(temperature_list)
    else:
        return jsonify({"error": f"{start} not found"})

# create the start/end route
@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    # create the session
    session = Session(engine)

    # query temperatures and calculate the minimum, average, and maximum temperature for
    # for the dates from the start date to the end date
    start_end_result = session.query(measurement.tobs,
                                 func.min(measurement.tobs), 
                                 func.max(measurement.tobs), 
                                 func.avg(measurement.tobs)).\
                                 filter(measurement.date >= start, measurement.date <= end).all()

    # make an empty list and store the dictionaries
    temperature_list = []
    for result in start_end_result:
        start_end_dict = {}
        start_end_dict['Minimum Temperature'] = result[1]
        start_end_dict['Maximum Temperature'] = result[2]
        start_end_dict['Average Temperature'] = result[3]
        temperature_list.append(start_end_dict)

    # jsonify and display the contents in the list
    if len(temperature_list) != 0:
        return jsonify(temperature_list)
    else:
        return jsonify({"error": f"{start} not found"})


# give the default name of the application so that we can start it from
# our command line
if __name__ == "__main__":
    app.run(port=5000, debug=True)
