
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

from model import Temperature

# not the proper way, but gets the job done
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db = SQLAlchemy()
db.init_app(app)

# will return lifetime average temp, can add since and until to query by time period
with app.app_context():
  db.create_all()
  temp = db.session.query(func.avg(Temperature.measurement).label('average')).filter(Temperature.location=='colony-1').first()
  print(temp) # returns the average temp
  # maybe a webhook to slack
  # SlackService.notify(temp)

# cronjob will look like
# 0 * * * * /path/to/pipenv /path/to/python cj.py