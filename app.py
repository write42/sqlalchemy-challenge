from flask import Flask, jsonify
import sqlalchemy
import pandas as pd
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect
from sqlalchemy import desc

engine = create_engine("sqlite:///hawaii.sqlite")
conn = engine.connect()

Base = automap_base()
Base.prepare(engine, reflect=True)
Base.classes.keys()

measurement = Base.classes.measurement
station = Base.classes.station

session = Session(engine)

inspector = inspect(engine)

df = pd.read_sql("SELECT date,prcp FROM measurement WHERE date > '2016-08-23'",conn)
df_next = df.dropna().sort_values("date")

app = Flask(__name__)

@app.route("/")
def home():
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation"
        f"/api/v1.0/stations"
        f"/api/v1.0/tobs"
        f"/api/v1.0/<start>"
        f"/api/v1.0/<start>/<end>"
    )
@app.route("/api/v1.0/precipitation")
def rain():
    all_rain=[]

    for date,prcp in df_next:
        rain_dict={}
        rain_dict["date"] = date
        rain_dict["prcp"] = prcp
        all_rain.append(rain_dict)
    return jsonify(all_rain)

@app.route("/api/v1.0/stations")
def station():
    station_count = list(session.query(station.station))
    return jsonify(station_count)

@app.route("/api/v1.0/tobs")
def temp():
    temp = pd.read_sql("SELECT station,tobs FROM measurement WHERE (date > '2016-08-23' AND station='USC00519281')",conn)
    temp = temp.dropna()
    temp
    return jsonify(temp)

@app.route("/api/v1.0/<start>")
def start():
    low_temp = session.query(measurement.station, func.min(measurement.tobs))\
            .group_by(measurement.station)\
            .order_by(func.count(measurement.station).desc()).first()
    high_temp = session.query(measurement.station, func.max(measurement.tobs))\
            .group_by(measurement.station)\
            .order_by(func.count(measurement.station).desc()).first()

    avg_temp = session.query(measurement.station, func.avg(measurement.tobs))\
            .group_by(measurement.station)\
            .order_by(func.count(measurement.station).desc()).first()
    return jsonify()

@app.route("/api/v1.0/<start>/<end>")
def end():
    low_temp = session.query(measurement.station, func.min(measurement.tobs))\
            .group_by(measurement.station)\
            .order_by(func.count(measurement.station).desc()).first()
    high_temp = session.query(measurement.station, func.max(measurement.tobs))\
            .group_by(measurement.station)\
            .order_by(func.count(measurement.station).desc()).first()

    avg_temp = session.query(measurement.station, func.avg(measurement.tobs))\
            .group_by(measurement.station)\
            .order_by(func.count(measurement.station).desc()).first()
    return jsonify()
    
if __name__ == "__main__":
    app.run(debug=True)    