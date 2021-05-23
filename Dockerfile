FROM python:3.8.0-buster

# Make a directory for our application
WORKDIR /application

# Install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Make a directory for persisting ETL data
RUN mkdir -p /etl/data

# Copy our source code
COPY etl.py .

# Run the ETL
CMD ["python","etl.py"]
