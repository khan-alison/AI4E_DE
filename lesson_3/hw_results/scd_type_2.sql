DROP TABLE IF EXISTS nnkhanh_schema.scd_type_2;

CREATE TABLE nnkhanh_schema.scd_type_2
(
    cust_id             VARCHAR,
    cust_nm             TEXT,
    birth_date          DATE,
    add_id              VARCHAR,
    opn_dt              DATE,
    end_dt              DATE,
    record_created_time DATE DEFAULT CURRENT_DATE,
    record_updated_time DATE DEFAULT '3000-12-12',
    record_is_active    BOOLEAN,
    record_change_type  VARCHAR,
    PRIMARY KEY (cust_id, record_created_time)
);

INSERT INTO nnkhanh_schema.scd_type_2 (cust_id, cust_nm, birth_date, add_id, opn_dt, end_dt, record_created_time,
                                       record_is_active, record_change_type)
SELECT cust_id,
       cust_nm,
       birth_date,
       add_id,
       opn_dt,
       end_dt,
       CURRENT_DATE,
       TRUE,
       'CDC_INSERT'
FROM ai4e_test.customer;

UPDATE nnkhanh_schema.scd_type_2 st2
SET record_updated_time = '2023-10-18',
    record_change_type  = 'CDC_UPDATE',
    record_is_active    = FALSE
FROM ai4e_test.customer_cdc_18 cc18
WHERE cc18.cust_id = st2.cust_id
  AND st2.record_is_active = TRUE;

INSERT INTO nnkhanh_schema.scd_type_2 (cust_id, cust_nm, birth_date, add_id, opn_dt, end_dt, record_created_time,
                                       record_is_active,
                                       record_change_type)
SELECT cust_id,
       cust_nm,
       birth_date,
       add_id,
       opn_dt,
       end_dt,
       '2023-10-18',
       TRUE,
       'CDC_INSERT'
FROM ai4e_test.customer_cdc_18;

UPDATE nnkhanh_schema.scd_type_2 st2
SET record_updated_time = '2023-10-19',
    record_is_active    = FALSE,
    record_change_type  = 'CDC_UPDATE'
FROM ai4e_test.customer_cdc_19 cc19
WHERE cc19.cust_id = st2.cust_id
  AND st2.record_is_active = TRUE;

INSERT INTO nnkhanh_schema.scd_type_2 (cust_id, cust_nm, birth_date, add_id, opn_dt, end_dt, record_created_time,
                                       record_is_active, record_change_type)
SELECT cust_id,
       cust_nm,
       birth_date,
       add_id,
       opn_dt,
       end_dt,
       '2023-10-19',
       TRUE,
       'CDC_INSERT'
FROM ai4e_test.customer_cdc_19
