# PYAPI

## Dependencies
- pipenv
- python 3.11.3

## Setup
1. `pipenv install`
2. `pipenv run flask run`
3. to test if working, execute:
```bash 
curl localhost:5000
```
4. to run test, execute:
```bash
pipenv run python test.py
```

## DB
- using sqlite3
- db file: `instance/database.db`, also preloaded with data
- schema

```sql
CREATE TABLE main.temperature (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    unit VARCHAR(64) NOT NULL,
    location VARCHAR(64) NOT NULL,
    measurement REAL NOT NULL,
    timestamp INTEGER NOT NULL
    timezone VARCHAR(64) NOT NULL
);
```

## API

- GET /temperature

query temperature measurements

params:
  - since: query by linux time
  - until: query by linux time (default now)
  - location: query by location
  - unit: query by unit
  - measurement: query by measurement, accepts json object with min and max keys

example:
  ```bash
  curl localhost:5000/temperature?unit=celcius&location=colony-1&since=1681895166&until=1681895168&measurement={"min": "1","max": "2"}
  ```

  - POST /temperature
    
  lets user add a temperature measurement

  request body:
  ```json
  {
    "unit": "celcius", 
    "location": "colony-1",
    "measurement": 20.0,
    "timestamp": 1681895166
  }
  ```
  
example:
```bash
curl -X POST -H "Content-Type: application/json" -d '{"unit": "celcius", "location": "colony-1", "measurement": 20.0, "timestamp": 1681895166}' localhost:5000/temperature
```

- GET /temperature/statistics

returns average, count, and sum of the temperature measurements

params:
  - since: query by linux time
  - until: query by linux time (default now)
  - location: query by location
  - unit: query by unit
  - measurement: query by measurement, accepts json object with min and max keys

example:
  ```bash
  curl localhost:5000/temperature?unit=celcius&location=colony-1&since=1681895166&until=1681895168
  ```

# Discussion
please refer to [this](https://github.com/heinrich10/pyapi/blob/main/DISCUSSION.md)