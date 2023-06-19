
from flask import request, jsonify
# from flask import current_app as app
from datetime import datetime

from app import app, db
from model import Temperature

@app.route('/')
def hello_world():
  return "<p>Hello, World!</p>"


@app.route('/temperature', methods=['GET'])
def get_temp():
  """
  since: query by time
  until: query by time
  location: query by location
  unit: query by unit
  measurement: query by measurement
  """
  params = request.args
  stmt = prepare_query_for_get_temp(params)
  rs = db.session.scalars(stmt).all()
  res = []
  for row in rs:
    res.append(to_dict(row))
  return jsonify(res)


@app.route('/temperature', methods=['POST'])
def post_temp():
  """
  will validate the request body and make sure location, unit, measurement, timestamp, timezone are present
  if not will tell the user what field is missing
  """
  try:
    body = request.json
    validate_post_temp(body)
    db.session.add(Temperature(**body))
    db.session.commit()
    return jsonify({"success": True})
  except Exception as e:
    return jsonify({"success": False, "errors": str(e)})


def to_dict(row):
  return {column.name: getattr(row, column.name) for column in row.__table__.columns if column.name != "id"}


def prepare_query_for_get_temp(params):
  query_filter = []
  if "location" in params:
    query_filter.append((Temperature.location == params["location"]))
  if "unit" in params:
    query_filter.append((Temperature.unit == params["unit"]))
  if "since" in params:
    query_filter.append((Temperature.timestamp >= params["since"]))
  if "until" in params:
    query_filter.append((Temperature.timestamp <= params["until"]))
  else:
    query_filter.append((Temperature.timestamp <= datetime.utcnow()))

  stmt = db.select(Temperature).where(*query_filter)
  return stmt


def validate_post_temp(body):
  errors = []
  if "timestamp" not in body:
    errors.append("timestamp is required")
  if "timezone" not in body:
    errors.append("timezone is required")
  if "measurement" not in body:
    errors.append("measurement is required")
  if "unit" not in body:
    errors.append("unit is required")
  if "location" not in body:
    errors.append("location is required")

  if errors:
    raise Exception(errors)
