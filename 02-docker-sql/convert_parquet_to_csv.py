import pyarrow.parquet as pq
import pandas as pd

from pathlib import Path


script_dir = Path(__file__).resolve().parent
input_file = script_dir / 'data' / 'yellow_tripdata_2024-01.parquet'
output_file = script_dir / 'data' / 'yellow_tripdata_2024-01.csv'

trips = pq.read_table(input_file)
trips = trips.to_pandas()

trips.to_csv(output_file, index=False)



