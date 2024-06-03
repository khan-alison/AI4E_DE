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

# Connect to the PostgreSQL database
conn = psycopg2.connect(
    host=DB_HOST,
    port=DB_PORT,
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD
)

# Create a cursor object
cur = conn.cursor()

# Create schema if not exists
cur.execute("""
CREATE SCHEMA IF NOT EXISTS nnkhanh_schema;
""")

# Drop existing tables if they exist
cur.execute("""
DROP TABLE IF EXISTS nnkhanh_schema.scd_type_2_py;
""")

# Create the SCD Type 2 table
cur.execute("""
CREATE TABLE nnkhanh_schema.scd_type_2_py (
    cust_id VARCHAR,
    cust_nm TEXT,
    birth_date DATE,
    add_id VARCHAR,
    opn_dt DATE,
    end_dt DATE,
    record_created_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    record_updated_time TIMESTAMP DEFAULT '3000-12-31',
    is_active BOOLEAN,
    PRIMARY KEY (cust_id, record_created_time)
);
""")
conn.commit()

# Read data from the existing tables into pandas DataFrames
customer_df = pd.read_sql_query("SELECT * FROM ai4e_test.customer", engine)
customer_cdc_18_df = pd.read_sql_query("SELECT * FROM ai4e_test.customer_cdc_18", engine)
customer_cdc_19_df = pd.read_sql_query("SELECT * FROM ai4e_test.customer_cdc_19", engine)


# Define a function to upsert data
def upsert_data(df, table_name):
    for index, row in df.iterrows():
        cust_id = row['cust_id']
        # Check if the customer exists and is active
        cur.execute(f"SELECT * FROM nnkhanh_schema.{table_name} WHERE cust_id = %s AND is_active = TRUE", (cust_id,))
        existing_record = cur.fetchone()

        if existing_record:
            # Update the existing record to mark it as inactive
            cur.execute(f"""
            UPDATE nnkhanh_schema.{table_name}
            SET is_active = FALSE, record_updated_time = CURRENT_TIMESTAMP
            WHERE cust_id = %s AND is_active = TRUE
            """, (cust_id,))
            conn.commit()

        # Insert the new record
        cur.execute(f"""
        INSERT INTO nnkhanh_schema.{table_name} (cust_id, cust_nm, birth_date, add_id, opn_dt, end_dt, record_created_time, is_active)
        VALUES (%s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP, TRUE)
        """, (cust_id, row['cust_nm'], row['birth_date'], row['add_id'], row['opn_dt'], row['end_dt']))
        conn.commit()


# Insert initial data
upsert_data(customer_df, 'scd_type_2_py')

# Update with data from customer_cdc_18
upsert_data(customer_cdc_18_df, 'scd_type_2_py')

# Update with data from customer_cdc_19
upsert_data(customer_cdc_19_df, 'scd_type_2_py')

# Close the cursor and connection
cur.close()
conn.close()
