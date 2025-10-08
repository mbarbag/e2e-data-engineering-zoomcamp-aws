## General notes & Commands

**Docker** is a set of *PaaS* (*you don't need to worry about infrastructure!*) products used to deliver software in packages called **containers**.

For data workflows, Docker allows us to package data applications, pipelines and their dependencies into **isolated containers**, ensuring they run consistently in different environments.

**For example**, you can use Docker to create a data platform on your machine.

**1. Each service runs in its own container**
  - **Postgres container** > database to store processed data.
  - **pgAdmin container** > web-based GUI tool used to interact with the Postgres database session.
  - **Dockerfile container** > a python script that ingest data into the Postgres DB.
    
**2. Docker Compose makes them "talk" to each other**
  - By default, Docker Compose creates a **private network**.
  - Containers can reach each other using this private network (e.g., `pgAdmin` can connect to `pgdabase:5432`).

After an image (*config snapshot*) is configured/defined, then you can run it through an instance of it (*container*). You can have multiple containers of the same image running in different environments (*Google, AWS, local pc, ...*).

### Docker-Compose 

Run it in detached mode:

```bash
docker-compose up -d
```

Shutting it down:

```bash
docker-compose down
```
### Dockerfile

Build the image:

```bash
docker build -t ingest_data:v00 .
```

Run it:

```bash
URL="https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2025-01.parquet"

docker run -it --network=docker_default ingest_data:v00 \
    --user=root \
    --password=root \
    --host=pgdatabase \
    --port=5432 \
    --db=ny_taxi \
    --tb=yellow_taxi_trips \
    --url=${URL}
```
