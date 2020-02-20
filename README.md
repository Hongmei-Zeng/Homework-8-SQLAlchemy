# Homework-8-SQLAlchemy

## According to the requirements, this Repo contains two main files:

### File climate_analysis.ipynb
The script fulfils Step 1 - Climate Analysis and Exploration

There are two plots produced along: 12mths_PrcpData.png and 12mths_TobData.png

### File Climate_App.py
The script takes Step 2 - Climate App

This task includes four routes:
* /api.v1.0/precipitation
* /api/v1.0/stations
* /api/v1.0/tobs
* /api/v1.0/vacation/<start_date>/<end_date>: 

  It takes "start_date" and/or "end_date" of the vacation

  e.g. api/v1.0/vacation?start_date=2016-11-21
 
  e.g. api/v1.0/vacation?start_date=2016-09-09&end_date=2017-01-01
