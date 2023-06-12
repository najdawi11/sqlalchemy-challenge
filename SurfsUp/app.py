# Import the dependencies.
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Measurement  = Base.classes.measurement 
Station  = Base.classes.station


# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################

app = Flask(__name__)


#################################################
# Flask Routes
#################################################

#roote homepage ROUTE 
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )


# Create a dictionary
prcp_dict = [
    {"date": "6/1/2010", "prcp ": "0.08"},
    {"date": "6/2/2010", "prcp ": "0"},
    {"date": "6/3/2010", "prcp ": " .1"},
    {"date": "6/4/2010", "prcp ": ".01"},
    {"date": "6/5/2010", "prcp ": ".09"},
    {"date": "6/6/2010", "prcp ": ".13"},
    {"date": "6/7/2010", "prcp ": ".44"}
]
#Return the PRCP data as json
@app.route("/api/v1.0/precipitation")
def prcp_r():
    """Return the prcp data as json"""

    return jsonify(prcp_dict)



station_l= [
    {"station": "USC00519397", "name ": "WAIKIKI 717.2, HI US"},
    {"station": "USC00513117", "name ": "KANEOHE 838.1, HI US"},
    {"station": "USC00514830", "name ": "KUALOA RANCH HEADQUARTERS 886.9, HI US"},
    {"station": "USC00517948", "name ": "PEARL CITY, HI US"},
    {"station": "USC00518838", "name ": "UPPER WAHIAWA 874.3, HI US"},
    {"station": "USC00519523", "name ": "WAIMANALO EXPERIMENTAL FARM, HI US"},
    {"station": "USC00519281", "name ": "WAIHEE 837.5, HI US"}
]

#Return the PRCP data as json
@app.route("/api/v1.0/stations")
def station_r():
    """Return the station data as json"""

    return jsonify(station_l)

#dectionary of most staions data 
station_l= [
    {"station": "USC00519397", "name ": "WAIKIKI 717.2, HI US"},
    {"station": "USC00513117", "name ": "KANEOHE 838.1, HI US"},
    {"station": "USC00514830", "name ": "KUALOA RANCH HEADQUARTERS 886.9, HI US"},
    {"station": "USC00517948", "name ": "PEARL CITY, HI US"},
    {"station": "USC00518838", "name ": "UPPER WAHIAWA 874.3, HI US"},
    {"station": "USC00519523", "name ": "WAIMANALO EXPERIMENTAL FARM, HI US"},
    {"station": "USC00519281", "name ": "WAIHEE 837.5, HI US"}
]

@app.route("/api/v1.0/tobs")
def tobs():
    # Create a session (link)
    session = Session(engine)

    results = session.query((Measurement.date),(Measurement.tobs)).filter(Measurement.station=="USC00519281").order_by(Measurement.date >="2016-08-23").all()
    session.close()
    # Convert list of dates and temperature observations into normal list
    active_stations = list(np.ravel(results))
    return jsonify(active_stations)

@app.route("/api/v1.0/start")
def start():
    start_date = input(f"Enter a start date.")
    # Create a session (link)
    session = Session(engine)
   
    results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs),func.avg(Measurement.tobs)).filter(Measurement.date >= start_date).all()
    session.close()
    # Convert list of tuples to a dictionary
    temp_start = []
    for Tmin, Tave, Tmax in results:
        temp_start_dict = {}
        temp_start_dict["TMIN"] = Tmin
        temp_start_dict["TAVE"] = Tave
        temp_start_dict["TMAX"] = Tmax
        temp_start.append(temp_start_dict)
    return jsonify (temp_start)




@app.route("/api/v1.0/start_to_end")
def start_to_end():
    start_date = input(f"Enter start date.")
    end_date = input(f"Enter end date.")
    # Create a session (link)
    session = Session(engine)
   
    results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs),func.avg(Measurement.tobs)).filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
    session.close()
    # Convert list into a dictionary
    temp_start_end = []
    for Tmin, Tave, Tmax in results:
        temp_start_end_dict = {}
        temp_start_end_dict["TMIN"] = Tmin
        temp_start_end_dict["TAVE"] = Tave
        temp_start_end_dict["TMAX"] = Tmax
        temp_start_end.append(temp_start_end_dict)
    return jsonify (temp_start_end)









if __name__ == '__main__':
    app.run(debug=True)
