# e2e-data-engineering-zoomcamp-aws

This repo contains my work following the Data Engineering Zoomcamp curriculum, adapted to AWS services instead of GCP. It’s a hands-on learning journey toward building data pipelines with modern tools.

## About the Dataset

This project uses the [NYC TLC Trip Record Data](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page), which contains detailed information on taxi trips in New York City, including pick-up and drop-off dates/times, locations, trip distances, fares, rate types, payment types, and driver-reported passenger counts.


## Docker

In the `docker/` folder remains all the Docker configuration.

**Docker Compose** is used to set up:
- A Postgres container (database)
- A pgAdmin container (UI)

The pgAdmin access service can communicate with Postgres through the **private network** created when running docker-compose.

The **Dockerfile** contains the ETL pipeline (*Python code*) to ingest data into that Postgres DB.


## Terraform

The `terraform/` folder contains all the Terraform setup required to create remote resources on AWS.

The `main.tf` file includes the provider configuration to connect to AWS and create an S3 bucket.

This configuration is intended to be executed from within an *EC2 instance* that has an IAM role attached with the appropriate permissions.


## Airflow

The `airflow/` folder contains all the orchestation configuration.

I decided to use *Airflow* insted of *Kestra* (which was originally used in the Data Engineering Zoomcamp) because it’s the tool I want to specialize in for the job market.

For educational purposes, we are going to simulate a real-world data flow from an application (Postgres → Redshift).

We will imagine that the Postgres database we previously built in the Docker module (by creating an ETL pipeline that extracts data from an external source) represents an **OLTP system** used to store *live* business data (*production data*) that is *periodically updated*.

Using **Apache Airflow**, we will orchestrate an **ELT pipeline** that extracts data from this Postgres database and loads it into **Redshift Serverless** for analytics and dashboarding.

**AWS S3** will act as the *staging layer* for *raw* data. Further transformations will be handled directly in the data warehouse, so we can take advantage of the MPP from the cloud data warehouse. 

This pipeline will be scheduled to run **daily**, ensuring that the Redshift Serverless data warehouse remains up to date.

### Architecture
> Extract (Postgres) **>>** Load raw data into S3 (staging layer) **>>** COPY raw data into Redshift (Data warehouse) **>>** Transform inside Redshift (*LATER* — SQL/dbt)

## dbt

In the `dbt/` folder remains all the **Transformation layer** from our ELT pipeline.

For this part, you'll need to configure the dbt project with a Redshift connection to your data warehouse. 
