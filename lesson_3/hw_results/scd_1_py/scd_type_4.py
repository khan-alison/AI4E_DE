import psycopg2
import pandas as pd
from sqlalchemy import create_engine

# Database connection parameters
DB_HOST = 'introduction-01-intro-ap-southeast-1-dev-introduction-db.cpfm8ml2cxp2.ap-southeast-1.rds.amazonaws.com'
DB_PORT = '5432'
DB_NAME = 'postgres'
DB_USER = 'postgres'
DB_PASSWORD = 'postgres123'

# Connection string for SQLAlchemy
conn_str = f'postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

# Create a SQLAlchemy engine
engine = create_engine(conn_str)

conn = psycopg2.connect(
    host=DB_HOST,
    port=DB_PORT,
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD
)

cur = conn.cursor()
# Create schema if not exists
cur.execute("""
CREATE SCHEMA IF NOT EXISTS nnkhanh_schema;
""")

# Drop existing tables if they exist
cur.execute("""DROP TABLE IF EXISTS nnkhanh_schema.scd_type_4_py""")
cur.execute("""DROP TABLE IF EXISTS nnkhanh_schema.scd_type_4_hist_py""")

cur.execute(
    """
    CREATE TABLE nnkhanh_schema.scd_type_4_py (
        cust_id VARCHAR PRIMARY KEY,
        cust_nm TEXT,
        birth_date DATE,
        add_id VARCHAR,
        opn_dt DATE,
        end_dt DATE,
        record_created_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """
)

cur.execute(
    """
    CREATE TABLE nnkhanh_schema.scd_type_4_hist_py (
        cust_id VARCHAR,
        cust_nm TEXT,
        birth_date DATE,
        add_id VARCHAR,
        opn_dt DATE,
        end_dt DATE,
        record_created_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        record_updated_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        is_active BOOLEAN,
        PRIMARY KEY (cust_id, record_created_time)
    )
    """
)

conn.commit()

# Read data from the existing tables into pandas DataFrames
customer_df = pd.read_sql_query("SELECT * FROM ai4e_test.customer", engine)
customer_cdc_18_df = pd.read_sql_query("SELECT * FROM ai4e_test.customer_cdc_18", engine)
customer_cdc_19_df = pd.read_sql_query("SELECT * FROM ai4e_test.customer_cdc_19", engine)


# Define a function to upsert data for SCD Type 4
def upsert_data(df, table_name, hist_table_name, change_type, batch_size=100):
    updates = []
    inserts = []
    for index, row in df.iterrows():
        cust_id = row['cust_id']
        # Check if the customer exists in the main table
        cur.execute(f"SELECT * FROM nnkhanh_schema.{table_name} WHERE cust_id = %s", (cust_id,))
        existing_record = cur.fetchone()

        if existing_record:
            # Prepare the update to be added to the batch
            updates.append((
                cust_id, existing_record[1], existing_record[2], existing_record[3], existing_record[4],
                existing_record[5],
                existing_record[6], change_type,
                row['cust_nm'], row['birth_date'], row['add_id'], row['opn_dt'], row['end_dt'], cust_id
            ))
        else:
            # Prepare the insert to be added to the batch
            inserts.append((
                cust_id, row['cust_nm'], row['birth_date'], row['add_id'], row['opn_dt'], row['end_dt']
            ))

        # Execute in batches
        if len(updates) >= batch_size or len(inserts) >= batch_size:
            execute_batch(updates, inserts, table_name, hist_table_name)
            updates = []
            inserts = []

    # Execute any remaining batches
    if updates or inserts:
        execute_batch(updates, inserts, table_name, hist_table_name)


def execute_batch(updates, inserts, table_name, hist_table_name):
    if updates:
        cur.executemany(f"""
            INSERT INTO nnkhanh_schema.{hist_table_name} (cust_id, cust_nm, birth_date, add_id, opn_dt, end_dt, record_created_time, record_updated_time, record_change_type)
            VALUES (%s, %s, %s, %s, %s, %s, %s, CURRENT_DATE, %s)
            """, [(
            u[0], u[1], u[2], u[3], u[4], u[5], u[6], u[7]
        ) for u in updates])

        cur.executemany(f"""
            UPDATE nnkhanh_schema.{table_name}
            SET cust_nm = %s, birth_date = %s, add_id = %s, opn_dt = %s, end_dt = %s, record_created_time = CURRENT_DATE
            WHERE cust_id = %s
            """, [(
            u[8], u[9], u[10], u[11], u[12], u[13]
        ) for u in updates])

    if inserts:
        cur.executemany(f"""
            INSERT INTO nnkhanh_schema.{table_name} (cust_id, cust_nm, birth_date, add_id, opn_dt, end_dt, record_created_time)
            VALUES (%s, %s, %s, %s, %s, %s, CURRENT_DATE)
            """, inserts)

    conn.commit()


# Insert initial data
upsert_data(customer_df, 'scd_type_4_py', 'scd_type_4_hist_py', 'CDC-INSERT')

# Update with data from customer_cdc_18
upsert_data(customer_cdc_18_df, 'scd_type_4_py', 'scd_type_4_hist_py', 'CDC-UPDATE')

# Update with data from customer_cdc_19
upsert_data(customer_cdc_19_df, 'scd_type_4_py', 'scd_type_4_hist_py', 'CDC-UPDATE')

# Close the cursor and connection
cur.close()
conn.close()

print("Data has been successfully inserted and updated.")