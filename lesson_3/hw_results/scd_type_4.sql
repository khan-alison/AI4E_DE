DROP TABLE IF EXISTS nnkhanh_schema.scd_type_4;
DROP TABLE IF EXISTS nnkhanh_schema.scd_type_4_hist;

CREATE TABLE nnkhanh_schema.scd_type_4
(
    cust_id             VARCHAR PRIMARY KEY,
    cust_nm             TEXT,
    birth_date          DATE,
    add_id              VARCHAR,
    opn_dt              DATE,
    end_dt              DATE,
    record_created_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE nnkhanh_schema.scd_type_4_hist
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

INSERT INTO nnkhanh_schema.scd_type_4 (cust_id, cust_nm, birth_date, add_id, opn_dt, end_dt, record_created_time)
SELECT cust_id, cust_nm, birth_date, add_id, opn_dt, end_dt, CURRENT_TIMESTAMP
FROM ai4e_test.customer;

INSERT INTO nnkhanh_schema.scd_type_4_hist (cust_id, cust_nm, birth_date, add_id, opn_dt, end_dt, record_created_time,
                                            record_updated_time, record_change_type)
SELECT cust_id,
       cust_nm,
       birth_date,
       add_id,
       opn_dt,
       end_dt,
       CURRENT_TIMESTAMP,
       '3000-1-1',
       'CDC-INSERT'
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
       CURRENT_TIMESTAMP,
       'CDC-UPDATE'
FROM nnkhanh_schema.scd_type_4
WHERE cust_id IN (SELECT cust_id
                  FROM ai4e_test.customer_cdc_18);

INSERT INTO nnkhanh_schema.scd_type_4 (cust_id, cust_nm, birth_date, add_id, opn_dt, end_dt, record_created_time)
SELECT CUST_ID, CUST_NM, BIRTH_DATE, ADD_ID, OPN_DT, END_DT, '2023-10-18'
FROM ai4e_test.customer_cdc_18
ON CONFLICT (cust_id) DO UPDATE
    SET cust_id             = excluded.cust_id,
        cust_nm             = excluded.cust_nm,
        birth_date          = excluded.birth_date,
        add_id              = excluded.add_id,
        opn_dt              = excluded.opn_dt,
        end_dt              = excluded.end_dt,
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
       CURRENT_TIMESTAMP,
       'CDC-UPDATE'
FROM nnkhanh_schema.scd_type_4
WHERE cust_id IN (SELECT cust_id
                  FROM ai4e_test.customer_cdc_19);

INSERT INTO nnkhanh_schema.scd_type_4 (cust_id, cust_nm, birth_date, add_id, opn_dt, end_dt, record_created_time)
SELECT cust_id, cust_nm, birth_date, add_id, opn_dt, end_dt, '2023-10-19'
FROM ai4e_test.customer_cdc_19
ON CONFLICT (cust_id)
    DO UPDATE SET cust_id             = excluded.cust_id,
                  cust_nm=excluded.cust_nm,
                  birth_date=excluded.birth_date,
                  add_id=excluded.add_id,
                  opn_dt=excluded.opn_dt,
                  end_dt=excluded.end_dt,
                  record_created_time = '2023-10-19';