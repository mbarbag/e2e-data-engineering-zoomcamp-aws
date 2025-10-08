# Use the official Pythoh 3.9.1 image as the base
FROM  python:3.9.1

# Install wget command
RUN apt-get install wget
# Install dependencies
RUN pip install pandas sqlalchemy psycopg2 pyarrow

# Set the working directory inside the container to /app
WORKDIR /app

# Copy the local file load-parquet-data.py inyo the container at /app
COPY load-parquet-data.py load-parquet-data.py

# Define the default command that runs when the container starts.
# It’s as if the container opens a shell and directly executes:
#    1. python
#    2. load-parquet-data.py
ENTRYPOINT ["python", "load-parquet-data.py"]
