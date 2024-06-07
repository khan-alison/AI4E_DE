DROP TABLE IF EXISTS nnkhanh_schema.scd_type_2;

CREATE TABLE nnkhanh_schema.scd_type_2
(
    cust_id             VARCHAR,
    cust_nm             TEXT,
    birth_date          DATE,
    add_id              VARCHAR,
    opn_dt              DATE,
    end_dt              DATE,
    record_created_time DATE,
    record_updated_time DATE DEFAULT '2030-12-12',
    record_change_type  VARCHAR,
    is_active           BOOLEAN
);

INSERT INTO nnkhanh_schema.scd_type_2 (cust_id, cust_nm, birth_date, add_id, opn_dt, end_dt, record_created_time,
                                       is_active, record_change_type)
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
    is_active           = FALSE
FROM ai4e_test.customer_cdc_18 cc18
WHERE st2.cust_id = cc18.cust_id
  AND st2.is_active = TRUE;

INSERT INTO nnkhanh_schema.scd_type_2 (cust_id, cust_nm, birth_date, add_id, opn_dt, end_dt, record_created_time,
                                       record_change_type, is_active)
SELECT cust_id,
       cust_nm,
       birth_date,
       add_id,
       opn_dt,
       end_dt,
       '2023-10-18',
       'CDC_INSERT',
       TRUE
FROM ai4e_test.customer_cdc_18;

UPDATE nnkhanh_schema.scd_type_2 st2
SET record_updated_time = '2023-10-19',
    record_change_type  = 'CDC_UPDATE',
    is_active           = FALSE
FROM ai4e_test.customer_cdc_19 cc19
WHERE st2.cust_id = cc19.cust_id
  AND st2.is_active = TRUE;

INSERT INTO nnkhanh_schema.scd_type_2 (cust_id, cust_nm, birth_date, add_id, opn_dt, end_dt, record_created_time,
                                       record_change_type, is_active)
SELECT cust_id,
       cust_nm,
       birth_date,
       add_id,
       opn_dt,
       end_dt,
       '2023-10-19',
       'CDC_INSERT',
       TRUE
FROM ai4e_test.customer_cdc_19;