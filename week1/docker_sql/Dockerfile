FROM python:3.12.8

# Install any needed packages
RUN apt-get install wget

RUN pip install pandas sqlalchemy psycopg2-binary

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY ingestData.py ingestData.py

# Run pipeline.py when the container launches
ENTRYPOINT ["python", "ingestData.py"]
