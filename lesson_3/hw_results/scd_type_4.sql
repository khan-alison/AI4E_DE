DROP TABLE IF EXISTS nnkhanh_schema.scd_type_4;
DROP TABLE IF EXISTS nnkhanh_schema.scd_type_4_hist;

CREATE TABLE nnkhanh_schema.scd_type_4
(
    cust_id           VARCHAR PRIMARY KEY ,
    cust_nm           TEXT,
    birth_date        DATE,
    add_id            VARCHAR,
    opn_dt            DATE,
    end_dt            DATE,
    record_created_time DATE DEFAULT CURRENT_DATE
);

CREATE TABLE nnkhanh_schema.scd_type_4_hist
(
    cust_id             VARCHAR,
    cust_nm             TEXT,
    birth_date          DATE,
    add_id              VARCHAR,
    opn_dt              DATE,
    end_dt              DATE,
    record_created_time DATE,
    record_updated_time DATE DEFAULT '2030-12-12',
    record_change_type  TEXT
);

INSERT INTO nnkhanh_schema.scd_type_4 (cust_id, cust_nm, birth_date, add_id, opn_dt, end_dt)
SELECT cust_id, cust_nm, birth_date, add_id, opn_dt, end_dt
FROM ai4e_test.customer;

INSERT INTO nnkhanh_schema.scd_type_4_hist (cust_id, cust_nm, birth_date, add_id, opn_dt, end_dt, record_created_time,
                                            record_change_type)
SELECT cust_id,
       cust_nm,
       birth_date,
       add_id,
       opn_dt,
       end_dt,
       CURRENT_DATE,
       'CDC_INSERT'
FROM ai4e_test.customer;

INSERT INTO nnkhanh_schema.scd_type_4_hist (cust_id, cust_nm, birth_date, add_id, opn_dt, end_dt, record_created_time,
                                            record_updated_time, record_change_type)
SELECT cust_id,
       cust_nm,
       birth_date,
       add_id,
       opn_dt,
       end_dt,
       record_created_time,
       CURRENT_DATE,
       'CDC_INSERT'
FROM nnkhanh_schema.scd_type_4
WHERE scd_type_4.cust_id IN (SELECT cc18.cust_id FROM ai4e_test.customer_cdc_18 cc18);

INSERT INTO nnkhanh_schema.scd_type_4 (cust_id, cust_nm, birth_date, add_id, opn_dt, end_dt, record_created_time)
SELECT cust_id, cust_nm, birth_date, add_id, opn_dt, end_dt, '2023-10-18'
FROM ai4e_test.customer_cdc_18
ON CONFLICT (cust_id) DO UPDATE SET cust_id           = EXCLUDED.cust_id,
                                    cust_nm           = EXCLUDED.cust_nm,
                                    birth_date        = EXCLUDED.birth_date,
                                    add_id            = EXCLUDED.add_id,
                                    opn_dt            = EXCLUDED.opn_dt,
                                    end_dt            = EXCLUDED.end_dt,
                                    record_created_time = '2023-10-18';

INSERT INTO nnkhanh_schema.scd_type_4_hist (cust_id, cust_nm, birth_date, add_id, opn_dt, end_dt, record_created_time,
                                            record_updated_time, record_change_type)
SELECT cust_id,
       cust_nm,
       birth_date,
       add_id,
       opn_dt,
       end_dt,
       record_created_time,
       CURRENT_DATE,
       'CDC_INSERT'
FROM nnkhanh_schema.scd_type_4
WHERE scd_type_4.cust_id IN (SELECT cc19.cust_id FROM ai4e_test.customer_cdc_19 cc19);

INSERT INTO nnkhanh_schema.scd_type_4 (cust_id, cust_nm, birth_date, add_id, opn_dt, end_dt, record_created_time)
SELECT cust_id, cust_nm, birth_date, add_id, opn_dt, end_dt, '2023-10-19'
FROM ai4e_test.customer_cdc_19
ON CONFLICT (cust_id) DO UPDATE SET cust_id           = EXCLUDED.cust_id,
                                    cust_nm           = EXCLUDED.cust_nm,
                                    birth_date        = EXCLUDED.birth_date,
                                    add_id            = EXCLUDED.add_id,
                                    opn_dt            = EXCLUDED.opn_dt,
                                    end_dt            = EXCLUDED.end_dt,
                                    record_created_time = '2023-10-19';