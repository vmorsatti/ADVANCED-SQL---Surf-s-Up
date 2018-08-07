
# Hawaii_app.py by Verna Orsatti
# Use in combination with db_prepare.py for boilerplate SQLalchemy 
from flask import Flask, json, jsonify
from db_prepare import engine, func, session, Measurement, Station

app = Flask(__name__)

# CLASSES
# measurement :  id ,  INTEGER
# measurement :  station ,  TEXT
# measurement :  date ,  TEXT
# measurement :  prcp ,  FLOAT
# measurement :  tobs ,  FLOAT
# station :  id ,  INTEGER
# station :  station ,  TEXT
# station :  name ,  TEXT
# station :  latitude ,  FLOAT
# station :  longitude ,  FLOAT
# station :  elevation ,  FLOAT

@app.route('/')
def home_route():
    """ Available API Route Endpoints"""
    return (f"Enter Available Route Endpoints.  Where dates are required, modify date selection as desired: <br><br/>"
        f"1.   2017 dates & temps dictionary:   <br/>"
        f"   /api/v1.0/precipitation/ <br><br/>" 
        f"2.   JSON list of stations:    <br/>"
        f" /api/v1.0/stations/ <br><br/>" 
        f"3.    2017 JSON list of Temp Observations:  <br/>"
        f" /api/v1.0/tobs/ <br><br/>"
        f"For the following, enter date as form 'yyyy' or 'yyyy-mm' or 'yyyy-mm-dd' for BEST RESULTS! <br><br/>"
        f"4.    Stats Combined Stations. Enter Start date:  <br/>"
        f" /api/v1.0/2016-01-01/ <br><br/>" 
        f"5.    Stats Combined Stations. Enter Start & End Date:  <br/>"
        f" /api/v1.0/2016-01-01/2016-12-31/ <br><br/>"
        f"BONUS Options for the interested! <br><br/>"
        f"6.    Stats by Station,  Enter Start date:    <br/>"
        f"  /api/v1.0/station/2017-01-01/ <br><br/>" 
        f"7.    Stats by Station,  Enter Start & End date:   <br/>"
        f"   /api/v1.0/station/2016-01-01/2016-12-31/ <end>")
        

#    Query Measurements for... All Stations
#    Dates and temperature observations from the last year.
#    Convert the query results to a Dictionary using 'date' as the key and 'tobs' as the value.
#    Return the JSON representation of your dictionary
@app.route('/api/v1.0/precipitation/')
def precipitation():
    prcp_results = session.query(Measurement.date, Measurement.tobs)\
    .filter(Measurement.date >= '2017-01-01').all()
    p_dict = dict(prcp_results)
    print()
    print("Results for Precipitation")
    return jsonify(p_dict) 


#    Query Stations for.... Stations
#    Return a JSON-list of stations from the dataset.
@app.route('/api/v1.0/stations/')
def stations():
    station_list = session.query(Station.station)\
    .order_by(Station.station).all() 
    print()
    print("Station List:")   
    for row in station_list:
        print (row[0])
    return jsonify(station_list)


#    Query Measurement for.... All stations
#    Return a JSON-list of Temperature Observations from the dataset.
@app.route('/api/v1.0/tobs/')
def tobs():
    temp_obs = session.query(Measurement.tobs)\
    .order_by(Measurement.date).all()
    print()
    print("Temperature Results for All Stations")
    return jsonify(temp_obs)


# Query Measurements for.... Combined Stations
# Return a JSON-list of Temperature Observations from the previous year.
#   /api/v1.0/<start  and /api/v1.0/<start>/<end>
#   Return JSON list of temps: minimum, average, maxium as TMIN TAVG TMAX
#       FOR A GIVEN START DATE OR START END RANGE
@app.route('/api/v1.0/<start>/')
def combined_start_stats(start):
    q = session.query(Station.id,
                  Station.station,
                  func.min(Measurement.tobs),
                  func.max(Measurement.tobs),
                  func.avg(Measurement.tobs))\
                  .filter(Measurement.station == Station.station)\
                  .filter(Measurement.date >= start).all()                  
    print()
    print("Query Temps Combinded Stations with Start ({start}) Date")
    for row in q:
        print()
        print(row)
    return jsonify(q)


# Query Measurements for.... Combined Stations
# Repeat of above stat request, but with end date added to decorator
@app.route('/api/v1.0/<start>/<end>/')
def combined_start_end_stats(start,end):
    q = session.query(Station.id,
                  Station.station,
                  func.min(Measurement.tobs),
                  func.max(Measurement.tobs),
                  func.avg(Measurement.tobs))\
                  .filter(Measurement.station == Station.station)\
                  .filter(Measurement.date <= end)\
                  .filter(Measurement.date >= start).all()
    print()
    print(f"Query Temps Combined Stations with Start ({start}) and End ({end}) Date")
    for row in q:
        print()
        print(row)
    return jsonify(q)

# BONUS options for the interested!

#    Query Measurements for.... by Station
#    Return a JSON-list of Temperature Observations from the previous year.
#   /api/v1.0/<start  and /api/v1.0/<start>/<end>
#   Return JSON list of temps: minimum, average, maxium as TMIN TAVG TMAX
#       FOR A GIVEN START DATE OR START END RANGE
@app.route('/api/v1.0/station/<start>/')
def station_start_stats(start):
    q = session.query(Station.id,
                  Station.station,
                  func.min(Measurement.tobs),
                  func.max(Measurement.tobs),
                  func.avg(Measurement.tobs))\
                  .filter(Measurement.station == Station.station)\
                  .filter(Measurement.date >= start)\
                  .group_by(Station.station)\
                  .order_by(Station.id).all()
    print()
    print("Query Temps for Stations with Start ({start}) Date")
    for row in q:
        print()
        print(row)
    return jsonify(q)

# Query Measurements for.... by Station
# Repeat of above stat request, but with end date added to decorator
@app.route('/api/v1.0/station/<start>/<end>/')
def station_start_end_stats(start,end):
    q = session.query(Station.id,
                  Station.station,
                  func.min(Measurement.tobs),
                  func.max(Measurement.tobs),
                  func.avg(Measurement.tobs))\
                  .filter(Measurement.station == Station.station)\
                  .filter(Measurement.date <= end)\
                  .filter(Measurement.date >= start)\
                  .group_by(Station.station)\
                  .order_by(Station.id).all()
    print()
    print(f"Query Temps for Stations with Start ({start}) and End ({end}) Date")
    for row in q:
        print()
        print(row)
    return jsonify(q)

app.run(debug=True)

# It was real... it was fun... but not real fun" ~anonymous quote from the '70s

# The end
