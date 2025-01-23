import pandas as pd

from pathlib import Path


dir = Path(__file__).resolve().parent
input_file = dir / 'data' / 'yellow_tripdata_2024-01.csv'

df = pd.read_csv(input_file)

print(df.info())