#!/usr/bin/env python
# coding: utf-8
import os
import pandas as pd
import argparse
from time import time
from sqlalchemy import create_engine


def main(params):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    tableName = params.tableName
    url = params.url

    csv_name = 'output.csv'

    # Download the data
    os.system(f"wget {url} -O {csv_name}.gz")
    # Unzip the file
    os.system(f"gunzip -c {csv_name}.gz > {csv_name}")

    # Create a connection to Postgres using SQLAlchemy
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')

    # Convert the DataFrame to a DDL format
    # print(pd.io.sql.get_schema(data, name='green_taxi_data', con=engine))

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

            print("Another chunk added!. Total time: %.3f" % (end-start))
        except StopIteration:
            print("Data ingestion completed!")
            break

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Ingest data into Postgres')
    parser.add_argument('--user', help='postgres user')
    parser.add_argument('--password', help='postgres password')
    parser.add_argument('--host', help='postgres host')
    parser.add_argument('--port', help='postgres port')
    parser.add_argument('--db', help='postgres db')
    parser.add_argument('--tableName', help='output table name')
    parser.add_argument('--url', help='csv url')

    args = parser.parse_args()
    main(args)