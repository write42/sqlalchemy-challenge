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
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )
@app.route("/api/v1.0/precipitation")
def rain():
    rain_date = session.query(measurement.date,measurement.prcp).order_by(measurement.date)
    rain_list=[]
    for row in rain_date:
        rain_dict={}
        rain_dict["date"] = row.date
        rain_dict["prcp"] = row.prcp
        rain_list.append(rain_dict)
    return jsonify(rain_list)

@app.route("/api/v1.0/stations")
def stations():
    station_count = list(session.query(station.station))
    return jsonify(station_count)

@app.route("/api/v1.0/tobs")
def temp():
    station_active = session.query(measurement.station, func.count(measurement.station))\
                .group_by(measurement.station)\
                .order_by(func.count(measurement.station).desc()).first()
    station_active_first = station_active[0]

    station_year = session.query(measurement.date, measurement.prcp).filter(measurement.station == station_active_first).filter(measurement.date >= '2016-08-23').all()
    return jsonify(station_year)

@app.route("/api/v1.0/<start>")
def start(begin):
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

#@app.route("/api/v1.0/<start>/<end>")
#def end(finish):
#    low_temp = session.query(measurement.station, func.min(measurement.tobs))\
#            .group_by(measurement.station)\
#            .order_by(func.count(measurement.station).desc()).first()
#    high_temp = session.query(measurement.station, func.max(measurement.tobs))\
#            .group_by(measurement.station)\
#            .order_by(func.count(measurement.station).desc()).first()

#   avg_temp = session.query(measurement.station, func.avg(measurement.tobs))\
#            .group_by(measurement.station)\
#            .order_by(func.count(measurement.station).desc()).first()
#    return jsonify()

if __name__ == "__main__":
    app.run(debug=True)    