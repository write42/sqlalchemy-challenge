from flask import Flask

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
    return jsonify()

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