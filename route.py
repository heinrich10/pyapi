from flask import request, jsonify
from datetime import datetime
from sqlalchemy import text
from json import loads

from app import app, db
from model import Temperature


@app.route('/')
def hello_world():
  return '<p>Hello, World!</p>'


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


@app.route('/temperature/statistics', methods=['GET'])
def get_temp_stats():
  """
  since: query by time
  until: query by time
  location: query by location
  unit: query by unit
  measurement: query by measurement
  returns the average, median, and count of the temperature measurements
  """
  params = request.args
  stmt, val = prepare_query_for_get_temp_stats(params)
  rs = db.session.execute(stmt, val).first()
  res = {
    "avg": rs[0] if rs[1] else 0,
    "count": rs[1],
    "median": rs[2] if rs[1] else 0
  }
  return jsonify(res)


# Helper functions below
def to_dict(row):
  return {column.name: getattr(row, column.name) for column in row.__table__.columns if column.name != 'id'}


def prepare_query_for_get_temp(params):
  query_filter = []
  if 'location' in params:
    query_filter.append((Temperature.location == params['location']))
  if 'unit' in params:
    query_filter.append((Temperature.unit == params['unit']))
  if 'measurement' in params:
    range = loads(params.get('measurement'))
    if 'min' in range:
      query_filter.append((Temperature.measurement >= range['min']))
    if 'max' in range:
      query_filter.append((Temperature.measurement <= range['max']))
  if 'since' in params:
    query_filter.append((Temperature.timestamp >= params['since']))
  if 'until' in params:
    query_filter.append((Temperature.timestamp <= params['until']))
  else:
    query_filter.append((Temperature.timestamp <= datetime.utcnow()))

  stmt = db.select(Temperature).where(*query_filter)
  return stmt


def prepare_query_for_get_temp_stats(req_params):
  status = False
  filter = 'WHERE '
  params = {}
  if 'location' in req_params:
    if status:
      filter += 'AND '
    filter += 'location = :location '
    params["location"] = req_params['location']
    status = True
  if 'unit' in req_params:
    if status:
      filter += 'AND '
    filter += 'unit = :unit '
    params["unit"] = req_params['unit']
    status = True

  if 'measurement' in req_params:
    range = loads(req_params.get('measurement'))
    if 'min' in range:
      if status:
        filter += 'AND '
      filter += 'measurement >= :min '
      params['min'] = range['min']
      status = True
    if 'max' in range:
      if status:
        filter += 'AND '
      filter += 'measurement <= :max '
      params['max'] = range['max']
      status = True

  if 'since' in req_params:
    if status:
      filter += 'AND '
    filter += 'timestamp >= :since '
    params['since'] = req_params['since']
    status = True

  if 'until' in req_params:
    if status:
      filter += 'AND '
    filter += 'timestamp <= :until '
    params['until'] = req_params['until']
  else:
    if status:
      filter += 'AND '
    filter += 'timestamp <= :until '
    params['until'] = datetime.utcnow()
    status = True

  qs = (
    f'SELECT '
    f'avg(measurement) as avg, '
    f'count(*) as count, '
    f'(SELECT AVG(measurement) FROM '
    f'(SELECT measurement FROM temperature {filter}ORDER BY measurement LIMIT 2 - '
    f'(SELECT COUNT(*) FROM temperature {filter}) % 2 OFFSET (SELECT (COUNT(*) - 1) / 2 FROM temperature {filter}))) as median '
    f'FROM temperature {filter}'
  )

  return text(qs), params


def validate_post_temp(body):
  errors = []
  if 'timestamp' not in body:
    errors.append('timestamp is required')
  if 'timezone' not in body:
    errors.append('timezone is required')
  if 'measurement' not in body:
    errors.append('measurement is required')
  if 'unit' not in body:
    errors.append('unit is required')
  if 'location' not in body:
    errors.append('location is required')

  if errors:
    raise Exception(errors)
