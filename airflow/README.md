## Setting Up Apache Airflow + PostgreSQL with Docker Compose

From the airflow folder, fetch the docker-compose.yaml from [Apache-Airflow official website](https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html#fetching-docker-compose-yaml).
```bash
wget https://airflow.apache.org/docs/apache-airflow/3.1.0/docker-compose.yaml
```
And adjust it based on what is needed. You can follow [this medium post](https://yesidays.medium.com/setting-up-apache-airflow-postgresql-with-docker-compose-2674a4d28055).

**What does it do *airflow db migrate* command in airflow-init?**

It connects to the Postgres DB (*defined in AIRFLOW__DATABASE__SQL_ALCHEMY_CONN*) and performs all necessary migrations.

So this command:
- Creates the Airflow metadata database (if it doesn’t exist).
- Applies the correct schema version for our Airflow version.
- Ensures all internal tables exist, e.g.: dag, task_instance, variable, connection, log, job, user, etc.

Basically, it builds the “brain” that Airflow uses to keep track of everything in our Postgres DB — DAG runs, tasks, logs, configs, etc.

**Prerequisites**

Make sure you alredy have:
- A Redshift Serverless workspace created.
- A database name, user, password and workgroup endpoint.

**Configure Airflow connections**

In Airflow UI go to http://localhost:8080 → Admin → Connections and add these:

- Postgres Connection
    - Conn ID: postgres_conn
    - Conn Type: Postgres
    - Host: pgdatabase
    - database: ny_taxi
    - Login: root
    - Password: root
    - Port: 5432
- AWS Connection
    - Conn ID: aws_conn
    - Conn Type: Amazon Web Services
- Redshift Connection
    - Conn ID: redshift_conn
    - Conn Type: Amazon Redshift
    - Host: <your_redshift_endpoint> (e.g. *workgroup-name.region.redshift-serverless.amazonaws.com*) Look for JDBC URL!
    - Schema: <your_redshift_db_name> (e.g. dev)
    - Login: <your_redshift_username> (e.g. admin)
    - Password: <your_redshift_password> (go to actions > edit admin credentials > manually add one)
    - Port: 5439

**Configure Airflow variables**

In Airflow UI go to http://localhost:8080 → Admin → Variables and add these:

- s3_bucket: <your_bucket_name>
- s3_key: <your_raw_data_file_name>
- table_name: yellow_taxi_trips
- iam_role_arn: <the_iam_role_arn_attached_to_redshift>

**Commands to run docker**

First, run Postgres service:
```
docker-compose up -d pgdatabase
```
Initialize Airflow:
```
docker-compose up airflow-init
```
Run the rest of services:
```
docker-compose up -d
```
Clean:
```
docker-compose down -v
sudo rm -rf logs/*
sudo rm -rf plugins/*
sudo rm -rf dags/*
```

**Steps to run Airflow**

1. Open Airflow UI (http://localhost:8080).
2. Turn on the DAG: etl_postgres_to_redshift_s3
3. Trigger it manually

**Other important commands**

To check the containers:
```
docker ps
```
To check the docker logs:
```
docker logs <container_name>
```

