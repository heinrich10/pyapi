
import unittest
from freezegun import freeze_time
from datetime import datetime

from route import validate_post_temp, prepare_query_for_get_temp_stats, prepare_query_for_get_temp

NOW = datetime.utcnow()

class TestValidatePostTemp(unittest.TestCase):
  def test_missing(self):
    body = {
      "unit": "C",
    }
    try:
      validate_post_temp(body)
    except Exception as e:
      self.assertEqual(str(e),
                       '[\'timestamp is required\', \'timezone is required\', \'measurement is required\', \'location is required\']',
                       'validation did not throw an exception')
  # test other fields and so on
  # def test_missing_unit(self):
  # def test_missing_location(self):
  # def test_missing_timestamp(self):
  # def test_missing_timezone(self):
  # def test_missing_measurement(self):

  def test_complete_body(self):
    body = {
      "timestamp": "2020-01-01 00:00:00",
      "timezone": "UTC",
      "measurement": 10,
      "unit": "C",
      "location": "test"
    }
    try:
      validate_post_temp(body)
    except Exception as e:
      self.assertEqual(e, None, 'validation threw an exception')

@freeze_time(NOW)
class TestPrepareQueryForGetTempStats(unittest.TestCase):
  def test_measurement_min_max(self):
    req_params = {
      'measurement': '{ "min": 10, "max": 20 }'
    }
    qs, params = prepare_query_for_get_temp_stats(req_params)
    self.assertEqual(str(qs), 'SELECT avg(measurement) as avg, count(*) as count, (SELECT AVG(measurement) '
                              'FROM (SELECT measurement FROM temperature WHERE measurement >= :min AND '
                              'measurement <= :max AND timestamp <= :until ORDER BY measurement LIMIT 2 - ('
                              'SELECT COUNT(*) FROM temperature WHERE measurement >= :min AND measurement <= :max AND '
                              'timestamp <= :until ) % 2 OFFSET (SELECT (COUNT(*) - 1) / 2 FROM temperature WHERE '
                              'measurement >= :min AND measurement <= :max AND timestamp <= :until ))) as median FROM '
                              'temperature WHERE measurement >= :min AND measurement <= :max AND timestamp <= :until ',
                     'wrong sql')
    self.assertEqual(params, {'min': 10, 'max': 20, 'until': NOW}, 'min and max params are incorrect')

  def test_measurement_min(self):
    req_params = {
      'measurement': '{ "min": 10 }'
    }
    qs, params = prepare_query_for_get_temp_stats(req_params)
    self.assertEqual(str(qs), 'SELECT avg(measurement) as avg, count(*) as count, (SELECT AVG(measurement) '
                              'FROM (SELECT measurement FROM temperature WHERE measurement >= :min '
                              'AND timestamp <= :until ORDER BY measurement LIMIT 2 - ('
                              'SELECT COUNT(*) FROM temperature WHERE measurement >= :min AND '
                              'timestamp <= :until ) % 2 OFFSET (SELECT (COUNT(*) - 1) / 2 FROM temperature WHERE '
                              'measurement >= :min AND timestamp <= :until ))) as median FROM '
                              'temperature WHERE measurement >= :min AND timestamp <= :until ',
                     'wrong sql')
    self.assertEqual(params, {'min': 10, 'until': NOW}, 'min and max params are incorrect')
  def test_measurement_max(self):
    req_params = {
      'measurement': '{ "max": 10 }'
    }
    qs, params = prepare_query_for_get_temp_stats(req_params)
    self.assertEqual(str(qs), 'SELECT avg(measurement) as avg, count(*) as count, (SELECT AVG(measurement) '
                              'FROM (SELECT measurement FROM temperature WHERE measurement <= :max ' 
                              'AND timestamp <= :until ORDER BY measurement LIMIT 2 - ('
                              'SELECT COUNT(*) FROM temperature WHERE measurement <= :max AND '
                              'timestamp <= :until ) % 2 OFFSET (SELECT (COUNT(*) - 1) / 2 FROM temperature WHERE '
                              'measurement <= :max AND timestamp <= :until ))) as median FROM '
                              'temperature WHERE measurement <= :max AND timestamp <= :until ',
                     'wrong sql')
    self.assertEqual(params, {'max': 10, 'until': NOW}, 'min and max params are incorrect')

  #   test each field and so on
  # def test_location(self):
  # def test_unit(self):
  # def test_since_until(self):
  # def test_since(self):
  # def test_until(self):

class TestPrepareQueryForGetTemp(unittest.TestCase):
  def test_measurement(self):
    req_params = {
      'measurement': '{ "min": 10, "max": 20 }'
    }
    stmt = prepare_query_for_get_temp(req_params)

    self.assertEqual(str(stmt),
"""SELECT temperature.id, temperature.timestamp, temperature.timezone, temperature.measurement, temperature.unit, temperature.location 
FROM temperature 
WHERE temperature.measurement >= :measurement_1 AND temperature.measurement <= :measurement_2 AND temperature.timestamp <= :timestamp_1""",
                     'wrong sql')

  def test_measurement_min(self):
    req_params = {
      'measurement': '{ "min": 10 }'
    }
    stmt = prepare_query_for_get_temp(req_params)

    self.assertEqual(str(stmt),
"""SELECT temperature.id, temperature.timestamp, temperature.timezone, temperature.measurement, temperature.unit, temperature.location 
FROM temperature 
WHERE temperature.measurement >= :measurement_1 AND temperature.timestamp <= :timestamp_1""",
                     'wrong sql')
  def test_measurement_max(self):
    req_params = {
      'measurement': '{ "max": 10 }'
    }
    stmt = prepare_query_for_get_temp(req_params)

    self.assertEqual(str(stmt),
"""SELECT temperature.id, temperature.timestamp, temperature.timezone, temperature.measurement, temperature.unit, temperature.location 
FROM temperature 
WHERE temperature.measurement <= :measurement_1 AND temperature.timestamp <= :timestamp_1""",
                     'wrong sql')

  #  test each field and so on

if __name__ == '__main__':
  unittest.main()