import pandas as pd
from sqlalchemy import create_engine

from pathlib import Path
from time import time

import extract_gz

data_dir = Path(__file__).resolve().parent
# input_file = data_dir / 'data' / 'green_tripdata_2019-10.csv.gz'
input_file = data_dir / 'data' / 'yellow_tripdata_2024-11.csv'

# df = pd.read_csv(extract_gz.unzip_gz_file(input_file), low_memory=False)
df = pd.read_csv(input_file, low_memory=False)

engine = create_engine('postgresql://root:root@localhost:5432/ny_taxi')


# create a db schema from csv structure - ddl
query = pd.io.sql.get_schema(df, name='yellow_taxi_data', con=engine)
print(query)

df_iter = pd.read_csv(input_file, low_memory=False, iterator=True, chunksize=100_000)
df = next(df_iter)

# convert types to usable
# df.lpep_pickup_datetime = pd.to_datetime(df.lpep_pickup_datetime)
# df.lpep_dropoff_datetime = pd.to_datetime(df.lpep_dropoff_datetime)

df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

df.head(n=0).to_sql(name='yellow_taxi_data', con=engine, if_exists='replace')

while True:
    try:
        t_start = time()

        df = next(df_iter)

        # convert types to usable
        # df.lpep_pickup_datetime = pd.to_datetime(df.lpep_pickup_datetime)
        # df.lpep_dropoff_datetime = pd.to_datetime(df.lpep_dropoff_datetime)

        df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
        df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

        df.to_sql(name='yellow_taxi_data', con=engine, if_exists='append')

        t_end = time()

        print('insert another chunk..., took %.3f sec' % (t_end - t_start))
    except StopIteration:
        print('End of inserting')
        break



