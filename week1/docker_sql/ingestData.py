#!/usr/bin/env python
# coding: utf-8
import os
import pandas as pd
import argparse
from time import time
from sqlalchemy import create_engine
import requests
import gzip
import shutil
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def download_and_decompress(url, output_path):
    """Download and decompress a gzipped CSV file."""
    try:
        logging.info(f"Downloading data from {url}")
        response = requests.get(url, stream=True)
        response.raise_for_status()
        with open(output_path, 'wb') as f_out:
            with gzip.GzipFile(fileobj=response.raw) as f_in:
                shutil.copyfileobj(f_in, f_out)
        logging.info(f"Downloaded and decompressed file to {output_path}")
    except Exception as e:
        logging.error(f"Error downloading or decompressing file: {e}")
        raise

def main(params):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    tableName = params.tableName
    url = params.url

    csv_name = 'output.csv'

    # Download and decompress the data
    download_and_decompress(url, csv_name)

    # Create a connection to Postgres using SQLAlchemy
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')

    # Specify data types for the columns
    dtype = {
        'VendorID': 'int64',
        'lpep_pickup_datetime': 'str',
        'lpep_dropoff_datetime': 'str',
        'store_and_fwd_flag': 'str',
        'RatecodeID': 'float64',
        'PULocationID': 'int64',
        'DOLocationID': 'int64',
        'passenger_count': 'float64',
        'trip_distance': 'float64',
        'fare_amount': 'float64',
        'extra': 'float64',
        'mta_tax': 'float64',
        'tip_amount': 'float64',
        'tolls_amount': 'float64',
        'ehail_fee': 'float64',
        'improvement_surcharge': 'float64',
        'total_amount': 'float64',
        'payment_type': 'float64',
        'trip_type': 'float64',
        'congestion_surcharge': 'float64'
    }

    # In order to ensure fast running time, the data will be divided into chunks of 100000 rows
    df_iter = pd.read_csv(csv_name, iterator=True, chunksize=100000, dtype=dtype)
    
    df = next(df_iter)
    df['lpep_pickup_datetime'] = pd.to_datetime(df['lpep_pickup_datetime'])
    df['lpep_dropoff_datetime'] = pd.to_datetime(df['lpep_dropoff_datetime'])

    # Insert data into Postgres table in chunks
    df.head(n=0).to_sql(name=tableName, con=engine, if_exists='replace')
    df.to_sql(name=tableName, con=engine, if_exists='append')

    while True:
        try:
            start = time()
            df = next(df_iter)
            df['lpep_pickup_datetime'] = pd.to_datetime(df['lpep_pickup_datetime'])
            df['lpep_dropoff_datetime'] = pd.to_datetime(df['lpep_dropoff_datetime'])

            df.to_sql(name=tableName, con=engine, if_exists='append')
            end = time()

            logging.info(f"Another chunk added! Total time: {end-start:.3f} seconds")
        except StopIteration:
            logging.info("Data ingestion completed!")
            break

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Ingest data into Postgres')
    parser.add_argument('--user', help='postgres user', required=True)
    parser.add_argument('--password', help='postgres password', required=True)
    parser.add_argument('--host', help='postgres host', required=True)
    parser.add_argument('--port', help='postgres port', required=True)
    parser.add_argument('--db', help='postgres db', required=True)
    parser.add_argument('--tableName', help='output table name', required=True)
    parser.add_argument('--url', help='csv url', required=True)

    args = parser.parse_args()
    main(args)