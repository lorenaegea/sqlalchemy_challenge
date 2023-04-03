# sqlalchemy_challenge
Module 10 Challenge - Georgia Institute of Technology Data Science and Analytics Boot Camp

Perform a climate analysis about Honolulu, Hawaii using Python and SQLAlchemy to explore a SQLite database. 
Design a Flask API based on the queries developed, with routes that include the following information:
- A precipitation route that returns json with the date as the key and the value as the precipitation, and only returns data for the last year in the database.
- A stations route that returns jsonified data of all of the stations in the database.
- A tobs route that returns jsonified data for the most active station (USC00519281), over the last year of data.
- A start route that accepts the start date as a parameter from the URL, and returns the min, max, and average temperatures calculated from the given start date to the end of the dataset.
- A start/end route that accepts the start and end dates as parameters from the URL, and returns the min, max, and average temperatures calculated from the given start date to the given end date.
