DROP TABLE IF EXISTS nnkhanh_schema.customer_scd_type_1;

CREATE TABLE nnkhanh_schema.customer_scd_type_1
(
    cust_id             VARCHAR PRIMARY KEY,
    cust_nm             TEXT,
    birth_date          DATE,
    add_id              VARCHAR,
    opn_dt              DATE,
    end_dt              DATE,
    record_created_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO nnkhanh_schema.customer_scd_type_1 (cust_id, cust_nm, birth_date, add_id, opn_dt, end_dt,
                                                record_created_time)
SELECT cust_id, cust_nm, birth_date, add_id, opn_dt, end_dt, CURRENT_TIMESTAMP
FROM ai4e_test.customer;

INSERT INTO nnkhanh_schema.customer_scd_type_1 (cust_id, cust_nm, birth_date, add_id, opn_dt, end_dt,
                                                record_created_time)
SELECT cust_id, cust_nm, birth_date, add_id, opn_dt, end_dt, CURRENT_TIMESTAMP
FROM ai4e_test.customer_cdc_18
ON CONFLICT (cust_id)
    DO UPDATE SET cust_nm             = EXCLUDED.cust_nm,
                  birth_date          = EXCLUDED.birth_date,
                  add_id              = EXCLUDED.add_id,
                  opn_dt              = EXCLUDED.opn_dt,
                  end_dt              = EXCLUDED.end_dt,
                  record_created_time = CURRENT_TIMESTAMP;

INSERT INTO nnkhanh_schema.customer_scd_type_1(cust_id, cust_nm, birth_date, add_id, opn_dt, end_dt,
                                               record_created_time)
SELECT cust_id, cust_nm, birth_date, add_id, opn_dt, end_dt, CURRENT_TIMESTAMP
FROM ai4e_test.customer_cdc_19
ON CONFLICT (cust_id)
DO UPDATE SET  cust_nm             = EXCLUDED.cust_nm,
                  birth_date          = EXCLUDED.birth_date,
                  add_id              = EXCLUDED.add_id,
                  opn_dt              = EXCLUDED.opn_dt,
                  end_dt              = EXCLUDED.end_dt,
                  record_created_time = CURRENT_TIMESTAMP;
