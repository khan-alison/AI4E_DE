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
DROP TABLE IF EXISTS nnkhanh_schema.customer_scd_type_1;
""")

# Create the SCD Type 1 table
cur.execute("""
CREATE TABLE nnkhanh_schema.customer_scd_type_1 (
    cust_id VARCHAR PRIMARY KEY,
    cust_nm TEXT,
    birth_date DATE,
    add_id VARCHAR,
    opn_dt DATE,
    end_dt DATE,
    record_created_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
""")
conn.commit()

# Read data from the existing tables into pandas DataFrames
customer_df = pd.read_sql_query("SELECT * FROM ai4e_test.customer", engine)
customer_cdc_18_df = pd.read_sql_query("SELECT * FROM ai4e_test.customer_cdc_18", engine)
customer_cdc_19_df = pd.read_sql_query("SELECT * FROM ai4e_test.customer_cdc_19", engine)


# Define a function to upsert data
def upsert_data(df, table_name):
    # Create a temporary table name
    tmp_table = f"tmp_{table_name}"

    # Drop the temporary table if it exists
    cur.execute(f"DROP TABLE IF EXISTS {tmp_table};")
    conn.commit()

    # Upload the DataFrame to the temporary table
    df.to_sql(tmp_table, engine, index=False, if_exists='replace', method='multi')

    # Upsert data from the temporary table to the target table
    upsert_query = f"""
    INSERT INTO nnkhanh_schema.{table_name} (cust_id, cust_nm, birth_date, add_id, opn_dt, end_dt, record_created_time)
    SELECT cust_id, cust_nm, birth_date, add_id, opn_dt, end_dt, CURRENT_TIMESTAMP
    FROM {tmp_table}
    ON CONFLICT (cust_id)
    DO UPDATE SET
        cust_nm = EXCLUDED.cust_nm,
        birth_date = EXCLUDED.birth_date,
        add_id = EXCLUDED.add_id,
        opn_dt = EXCLUDED.opn_dt,
        end_dt = EXCLUDED.end_dt,
        record_created_time = EXCLUDED.record_created_time;
    """
    cur.execute(upsert_query)
    conn.commit()


# Insert initial data
upsert_data(customer_df, 'customer_scd_type_1')

# Update with data from customer_cdc_18
upsert_data(customer_cdc_18_df, 'customer_scd_type_1')

# Update with data from customer_cdc_19
upsert_data(customer_cdc_19_df, 'customer_scd_type_1')

# Close the cursor and connection
cur.close()
conn.close()
