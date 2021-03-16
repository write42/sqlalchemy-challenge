from flask import Flask
import sqlalchemy
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

all_rain=[]

for date,prcp in df_next:
    rain_dict={}
    rain_dict["date"] = date
    rain_dict["prcp"] = prcp
    all_rain.append(rain_dict)

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
    return jsonify(all_rain)

@app.route("/api/v1.0/stations")
def station():
    return jsonify()

@app.route("/api/v1.0/tobs")
def temp():
    return jsonify()

@app.route("/api/v1.0/<start>")
def start():

@app.route("/api/v1.0/<start>/<end>")
def end():

if __name__ == "__main__":
    app.run(debug=True)    