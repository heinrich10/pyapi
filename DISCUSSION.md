# Discussion

- it is usually better to use request params (?unit=celsius) rather than path params (/temperature/<unit>). some of the reasons are:
  - it is easier to read, something like `/temperature/celsius/colony-1` does not make much sense
  - more intuitive for the user
  - and usually a path would return 1 resource, while a query would return a list of resources
- not much of a relational db type of thing because it only has 1 entity
- use timezone to display time in the user's local time (did not implement this)
- have to use raw sql to compute for statistics


# Notes

- for simplicity's sake, using the following tech:
  - pipenv: easy to setup and use, also dependency is not bad
  - flask: one of the more famous python web frameworks and simpler than for example django
  - alchemy: better to use some db framework so that it has built in session management
  - sqlite3: has most sql functionality, no need to setup a proper db server
- datatypes not optimized since sqlite3 is used

# Bonus
- unit test: partial implementation on test.py
- caching: not implemented
- rate limit: it is still a good idea to do rate limiting on the api gateway side
- hourly notification: refer to `cj.py`, if it is simple like this, cronjob will still be the best way to handle it
if there is a more complex use case, we can use message queues