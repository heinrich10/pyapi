from datetime import datetime
from app import db

class Temperature(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  timestamp = db.Column(db.Integer, default=datetime.utcnow)
  timezone = db.Column(db.String(64), nullable=False)
  measurement = db.Column(db.Float, nullable=False)
  unit = db.Column(db.String(64), nullable=False)
  location = db.Column(db.String(64), nullable=False)

  def __init__(self, timestamp, timezone, measurement, unit, location):
    self.timestamp = timestamp
    self.timezone = timezone
    self.measurement = measurement
    self.unit = unit
    self.location = location

  def __repr__(self):
    return f"Temperature('{self.id}, {self.measurement}')"
