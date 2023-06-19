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
params:
  - since: query by linux time
  - until: query by linux time (default now)
  - location: query by location
  - unit: query by unit
  - measurement: query by measurement

example:
  ```commandline
  curl localhost:5000/temperature?unit=celcius&location=colony-1&since=1681895166&until=1681895168
  ```
  - POST /temperature
    
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