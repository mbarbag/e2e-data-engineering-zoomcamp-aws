# e2e-data-engineering-zoomcamp-aws
This repo contains my work following the Data Engineering Zoomcamp curriculum, adapted to AWS services instead of GCP. It’s a hands-on learning journey toward building data pipelines with modern tools.

## About the Dataset

This project uses the [NYC TLC Trip Record Data](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page), which contains detailed information on taxi trips in New York City, including pick-up and drop-off dates/times, locations, trip distances, fares, rate types, payment types, and driver-reported passenger counts.

## Docker

On the `docker/` folder remains all the Docker configuration.

**Docker Compose** is used to set up:
- A Postgres container (database)
- A pgAdmin container (UI)

The pgAdmin access service can communicate with Postgres through the **private network** created when running docker-compose.

The **Dockerfile** contains the ETL pipeline (*Python code*) to ingest data into that Postgres DB.
