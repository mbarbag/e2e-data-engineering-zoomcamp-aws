from airflow import DAG
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from airflow.providers.amazon.aws.hooks.redshift_sql import RedshiftSQLHook
from airflow.operators.python import PythonOperator
from datetime import datetime
from time import time
import io
from airflow.models import Variable
import pyarrow as pa
import pyarrow.parquet as pq

S3_BUCKET = Variable.get("s3_bucket")
S3_KEY = Variable.get("s3_key")
TABLE_NAME = Variable.get("table_name")
IAM_ROLE = Variable.get("iam_role_arn")

def extract_from_postgres_to_s3(**context):
    # get data from postgres in chunks
    sql = "SELECT * FROM yellow_taxi_trips;"
    postgres_hook = PostgresHook(postgres_conn_id="postgres_conn")
    postgres_iter = postgres_hook.get_pandas_df_by_chunks(sql=sql, chunksize=100000)

    buffer = io.BytesIO()
    parquet_writer = None

    schema = pa.schema([
        ('VendorID', pa.int32()),
        ('tpep_pickup_datetime', pa.timestamp('us')),
        ('tpep_dropoff_datetime', pa.timestamp('us')),
        ('passenger_count', pa.int32()),
        ('trip_distance', pa.float32()),
        ('RatecodeID', pa.int32()),
        ('store_and_fwd_flag', pa.string()),
        ('PULocationID', pa.int32()),
        ('DOLocationID', pa.int32()),
        ('payment_type', pa.int32()),
        ('fare_amount', pa.float32()),
        ('extra', pa.float32()),
        ('mta_tax', pa.float32()),
        ('tip_amount', pa.float32()),
        ('tolls_amount', pa.float32()),
        ('improvement_surcharge', pa.float32()),
        ('total_amount', pa.float32()),
        ('congestion_surcharge', pa.float32()),
        ('Airport_fee', pa.float32()),
        ('cbd_congestion_fee', pa.float32())
    ])

    t_start = time()
    n=0
    total_rows = 0
    for batch in postgres_iter:
        n+=1
        total_rows += len(batch)
        print(f"Processing batch {n}... \n")
        b_start = time()
        table = pa.Table.from_pandas(batch, schema=schema)
        if parquet_writer is None:
            parquet_writer = pq.ParquetWriter(buffer, schema, compression='snappy')
        parquet_writer.write_table(table)
        
        b_end = time()
        print(f'Time taken: {b_end-b_start:10.3f} seconds.\n')


    if parquet_writer:
        parquet_writer.close()

    buffer.seek(0)
    
    t_end = time()
    print(f'Parquet file created! \n')
    print(f'Total time taken: {t_end-t_start:10.3f} seconds for {n} batches.\n')
    print(f'Total rows: {total_rows:,} \n')

    # upload to s3
    print(f'Uploading to S3: s3://{S3_BUCKET}/{S3_KEY}')
    s3_hook = S3Hook(aws_conn_id="aws_conn")
    u_start = time()
    s3_hook.load_bytes(buffer.getvalue(), key=S3_KEY, bucket_name=S3_BUCKET, replace=True)
    u_end = time()
    print(f"Uploaded {S3_KEY} to {S3_BUCKET} in {u_end-u_start:10.3f} seconds.\n")

def load_into_redshift(**context):
    s3_path = f"s3://{S3_BUCKET}/{S3_KEY}"
    redshift_hook = RedshiftSQLHook(redshift_conn_id="redshift_conn")

    drop_sql = f"DROP TABLE IF EXISTS {TABLE_NAME};"
    create_sql = f"""
        CREATE TABLE {TABLE_NAME} (
        VendorID INTEGER,
        tpep_pickup_datetime TIMESTAMP,
        tpep_dropoff_datetime TIMESTAMP,
        passenger_count INTEGER,
        trip_distance REAL,
        RatecodeID INTEGER,
        store_and_fwd_flag TEXT,
        PULocationID INTEGER,
        DOLocationID INTEGER,
        payment_type INTEGER,
        fare_amount REAL,
        extra REAL,
        mta_tax REAL,
        tip_amount REAL,
        tolls_amount REAL,
        improvement_surcharge REAL,
        total_amount REAL,
        congestion_surcharge REAL,
        Airport_fee REAL,
        cbd_congestion_fee REAL
        );
    """
    copy_sql = f"""
        COPY {TABLE_NAME}
        FROM '{s3_path}'
        IAM_ROLE '{IAM_ROLE}'
        FORMAT AS PARQUET;
    """

    redshift_hook.run(drop_sql)
    redshift_hook.run(create_sql)
    redshift_hook.run(copy_sql)
    print(f"Data successfully loaded into Redshift table {TABLE_NAME}")

with DAG(
    dag_id="etl_postgres_s3_redshift",
    start_date=datetime(2025,10,17),
    schedule_interval='@daily',
    catchup=False,
) as dag:
    
    extract = PythonOperator(
        task_id="extract_postgres",
        python_callable=extract_from_postgres_to_s3,
        provide_context=True
    )

    load = PythonOperator(
        task_id="load_redshift",
        python_callable=load_into_redshift,
        provide_context=True
    )

    extract >> load
