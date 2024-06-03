-- Step 1: Create Table
DROP TABLE IF EXISTS nnkhanh_schema.customer_scd_type_2;

CREATE TABLE nnkhanh_schema.customer_scd_type_2
(
    cust_id             VARCHAR,
    cust_nm             TEXT,
    birth_date          DATE,
    add_id              VARCHAR,
    opn_dt              DATE,
    end_dt              DATE,
    record_created_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    record_updated_time TIMESTAMP DEFAULT '3000-12-12',
    record_is_active    BOOLEAN,
    record_change_type  VARCHAR,
    PRIMARY KEY (cust_id, record_created_time)
);

-- Step 2: Insert Initial Data
INSERT INTO nnkhanh_schema.customer_scd_type_2 (cust_id, cust_nm, birth_date, add_id, opn_dt, end_dt,
                                                record_created_time, record_is_active, record_change_type)
SELECT cust_id,
       cust_nm,
       birth_date,
       add_id,
       opn_dt,
       end_dt,
       CURRENT_TIMESTAMP,
       TRUE,
       'CDC_INSERT'
FROM ai4e_test.customer;

-- Step 3: Insert Data from customer_cdc_18
-- Update existed ones
UPDATE nnkhanh_schema.customer_scd_type_2 cst2
SET record_is_active    = FALSE,
    record_updated_time = CURRENT_TIMESTAMP,
    record_change_type  = 'CDC_UPDATE'
FROM ai4e_test.customer_cdc_18 cdc
WHERE cst2.cust_id = cdc.cust_id
  AND cst2.record_is_active = TRUE;

-- Insert records
INSERT INTO nnkhanh_schema.customer_scd_type_2 (cust_id, cust_nm, birth_date, add_id, opn_dt, end_dt,
                                                record_created_time, record_is_active,
                                                record_change_type)
SELECT cust_id,
       cust_nm,
       birth_date,
       add_id,
       opn_dt,
       end_dt,
       CURRENT_TIMESTAMP,
       TRUE,
       'CDC_INSERT'
FROM ai4e_test.customer_cdc_18;

-- Step 4: Add data from customer_cdc_19 to the scd_type_2 table
-- Update existed ones
UPDATE nnkhanh_schema.customer_scd_type_2 sct2
SET record_is_active    = FALSE,
    record_change_type  = 'CDC_UPDATE',
    record_updated_time = CURRENT_TIMESTAMP
FROM ai4e_test.customer_cdc_19 cdc
WHERE sct2.cust_id = cdc.cust_id
  AND sct2.record_is_active = TRUE;

-- Insert not existed ones:
INSERT INTO nnkhanh_schema.customer_scd_type_2 (cust_id, cust_nm, birth_date, add_id, opn_dt, end_dt,
                                                record_created_time, record_is_active,
                                                record_change_type)

SELECT cust_id,
       cust_nm,
       birth_date,
       add_id,
       opn_dt,
       end_dt,
       CURRENT_TIMESTAMP,
       TRUE,
       'CDC_INSERT'
FROM ai4e_test.customer_cdc_19;

select count(1) from nnkhanh_schema.customer_scd_type_2;