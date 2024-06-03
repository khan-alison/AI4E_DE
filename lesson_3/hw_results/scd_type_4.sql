-- Step 1: Create Schema and Tables
DROP TABLE IF EXISTS nnkhanh_schema.customer_scd_type_4;
DROP TABLE IF EXISTS nnkhanh_schema.customer_scd_type_4_hist;

-- Create the current data table
CREATE TABLE nnkhanh_schema.customer_scd_type_4
(
    cust_id             VARCHAR PRIMARY KEY,
    cust_nm             TEXT,
    birth_date          DATE,
    add_id              VARCHAR,
    opn_dt              DATE,
    end_dt              DATE,
    record_created_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create the historical data table
CREATE TABLE nnkhanh_schema.customer_scd_type_4_hist
(
    cust_id             VARCHAR,
    cust_nm             TEXT,
    birth_date          DATE,
    add_id              VARCHAR,
    opn_dt              DATE,
    end_dt              DATE,
    record_created_time TIMESTAMP,
    record_updated_time TIMESTAMP,
    record_change_type  VARCHAR,
    PRIMARY KEY (cust_id, record_created_time)
);

-- Step 2: Insert Initial Data
-- Insert into current data table
INSERT INTO nnkhanh_schema.customer_scd_type_4 (cust_id, cust_nm, birth_date, add_id, opn_dt, end_dt,
                                                record_created_time)
SELECT cust_id, cust_nm, birth_date, add_id, opn_dt, end_dt, CURRENT_TIMESTAMP
FROM ai4e_test.customer;

-- Insert into historical data table
INSERT INTO nnkhanh_schema.customer_scd_type_4_hist (cust_id, cust_nm, birth_date, add_id, opn_dt, end_dt,
                                                     record_created_time, record_updated_time, record_change_type)
SELECT cust_id,
       cust_nm,
       birth_date,
       add_id,
       opn_dt,
       end_dt,
       CURRENT_TIMESTAMP,
       '3000-12-12',
       'CDC_INSERT'
FROM ai4e_test.customer;

-- Step 3: Update with Data from customer_cdc_18
-- Step 3.1: Insert old records into historical table with updated time
INSERT INTO nnkhanh_schema.customer_scd_type_4_hist (cust_id, cust_nm, birth_date, add_id, opn_dt, end_dt,
                                                     record_created_time, record_updated_time, record_change_type)
SELECT cust_id,
       cust_nm,
       birth_date,
       add_id,
       opn_dt,
       end_dt,
       record_created_time,
       CURRENT_TIMESTAMP,
       'CDC_UPDATE'
FROM nnkhanh_schema.customer_scd_type_4
WHERE cust_id IN (SELECT cust_id FROM ai4e_test.customer_cdc_18);

INSERT INTO nnkhanh_schema.customer_scd_type_4 (cust_id, cust_nm, birth_date, add_id, opn_dt, end_dt,
                                                record_created_time)
SELECT cust_id, cust_nm, birth_date, add_id, opn_dt, end_dt, CURRENT_TIMESTAMP
FROM ai4e_test.customer_cdc_18
ON CONFLICT (cust_id)
    DO UPDATE SET cust_id   = excluded.cust_id,
                  cust_nm=excluded.cust_nm,
                  birth_date=excluded.birth_date,
                  add_id=excluded.add_id,
                  opn_dt=excluded.opn_dt,
                  end_dt=excluded.end_dt,
                  record_created_time = CURRENT_TIMESTAMP;

-- Step 3: Update with Data from customer_cdc_19
-- Step 3.1: Insert old records into historical table with updated time
INSERT INTO nnkhanh_schema.customer_scd_type_4_hist (cust_id, cust_nm, birth_date, add_id, opn_dt, end_dt,
                                                     record_created_time, record_updated_time, record_change_type)
SELECT cust_id,
       cust_nm,
       birth_date,
       add_id,
       opn_dt,
       end_dt,
       record_created_time,
       CURRENT_TIMESTAMP,
       'CDC_UPDATE'
FROM nnkhanh_schema.customer_scd_type_4
WHERE cust_id IN (SELECT cust_id FROM ai4e_test.customer_cdc_19);

INSERT INTO nnkhanh_schema.customer_scd_type_4 (cust_id, cust_nm, birth_date, add_id, opn_dt, end_dt,
                                                record_created_time)
SELECT cust_id, cust_nm, birth_date, add_id, opn_dt, end_dt, CURRENT_TIMESTAMP
FROM ai4e_test.customer_cdc_19
ON CONFLICT (cust_id)
    DO UPDATE SET cust_id   = excluded.cust_id,
                  cust_nm=excluded.cust_nm,
                  birth_date=excluded.birth_date,
                  add_id=excluded.add_id,
                  opn_dt=excluded.opn_dt,
                  end_dt=excluded.end_dt,
                  record_created_time = CURRENT_TIMESTAMP;