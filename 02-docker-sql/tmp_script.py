import psycopg2
import os

# Database connection parameters
DB_SETTINGS = {
    "dbname": "ny_taxi",
    "user": "root",
    "password": "root",
    "host": "localhost",
    "port": 5432,
}

# The path to files
DATA_FOLDER = "data"
FILES = {
    "green_tripdata_2019_10.csv": """
        CREATE TABLE IF NOT EXISTS green_tripdata_2019_10 (
            VendorID INT,
            lpep_pickup_datetime TIMESTAMP,
            lpep_dropoff_datetime TIMESTAMP,
            store_and_fwd_flag VARCHAR(10),
            RatecodeID INT,
            PULocationID INT,
            DOLocationID INT,
            passenger_count INT,
            trip_distance FLOAT,
            fare_amount FLOAT,
            extra FLOAT,
            mta_tax FLOAT,
            tip_amount FLOAT,
            tolls_amount FLOAT,
            ehail_fee FLOAT,
            improvement_surcharge FLOAT,
            total_amount FLOAT,
            payment_type INT,
            trip_type INT,
            congestion_surcharge FLOAT
        );
    """,
    "taxi_zone_lookup.csv": """
        CREATE TABLE IF NOT EXISTS taxi_zone_lookup (
            LocationID INT PRIMARY KEY,
            Borough VARCHAR(50),
            Zone VARCHAR(100),
            service_zone VARCHAR(50)
        );
    """,
}

def create_table_and_load_data(conn, file_name, create_table_query):
    """Creating a table and downloading data from CSV."""
    table_name = file_name.split(".")[0]

    with conn.cursor() as cursor:
        print(f"Create table {table_name}...")
        cursor.execute(create_table_query)
        conn.commit()

        # Download data
        file_path = os.path.join(DATA_FOLDER, file_name)
        print(f"Download data from a file {file_name}...")
        with open(file_path, "r") as f:
            cursor.copy_expert(
                f"COPY {table_name} FROM STDIN WITH CSV HEADER", f
            )
        conn.commit()
        print(f"ДData from the {file_name} file is successfully uploaded to the {table_name} table!")

def main():
    # Connection to the database!
    try:
        conn = psycopg2.connect(**DB_SETTINGS)
        print("Successful connection to the database!")

        for file_name, create_table_query in FILES.items():
            create_table_and_load_data(conn, file_name, create_table_query)

    except Exception as e:
        print(f"Connection or operation error: {e}")

    finally:
        if conn:
            conn.close()
            print("Connection close.")

if __name__ == "__main__":
    main()
