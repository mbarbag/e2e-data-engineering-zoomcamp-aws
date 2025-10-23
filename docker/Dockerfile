# Use the official Pythoh 3.9 image as the base
FROM  python:3.9

# Install dependencies (in this case, only pandas)
RUN pip install pandas

# Set the working directory inside the container to /app
WORKDIR /app

# Copy the local file pipeline.py inyo the container at /app
COPY pipeline.py pipeline.py

# Define the default command that runs when the container starts.
# It’s as if the container opens a shell and directly executes:
#    1. python
#    2. pipeline.py
ENTRYPOINT ["python", "pipeline.py"]
