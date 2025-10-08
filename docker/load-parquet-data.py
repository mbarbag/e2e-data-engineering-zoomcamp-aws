import pyarrow.parquet as pq
import pandas as pd
from sqlalchemy import create_engine
from time import time
import argparse
import os

def main(params):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    tb = params.tb
    url = params.url

    file_name = os.path.basename(url)
    os.system(f"wget {url} -O {file_name}")

    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')

    parquet_file = pq.ParquetFile(file_name)
    parquet_iter = parquet_file.iter_batches(batch_size=100000)

    n = 0
    t_start = time()
    for batch in parquet_iter:
        if n == 0:
            print('Ingesting batch 1...')
            b_start = time()
            df_batch = batch.to_pandas()
            df_batch.to_sql(name=tb, con=engine, if_exists='replace')
            b_end = time()
            print(f'Time taken: {b_end-b_start:10.3f} seconds.\n')
            n+=1
            continue

        n+=1
        print(f'Ingesting batch {n}...')
        b_start = time()
        df_batch = batch.to_pandas()
        df_batch.to_sql(name=tb, con=engine, if_exists='append')
        b_end = time()
        print(f'Time taken: {b_end-b_start:10.3f} seconds.\n')

    t_end = time()  
    print(f'The ingestion is finished! Total time taken: {t_end-t_start:10.3f} seconds for {n} batches.') 



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Ingest downloaded .parquet data to Postgres')

    parser.add_argument('--user', required=True, help='Username for Postgres.')
    parser.add_argument('--password', required=True, help='Password for Postgres.')
    parser.add_argument('--host', required=True, help='Hostname for Postgres.')
    parser.add_argument('--port', required=True, help='Port for Postgres connection.')
    parser.add_argument('--db', required=True, help='Database name for Postgres.')
    parser.add_argument('--tb', required=True, help='Destination table name for Postgres.')
    parser.add_argument('--url', required=True, help='URL for .parquet file.')

    args = parser.parse_args()
    main(args)