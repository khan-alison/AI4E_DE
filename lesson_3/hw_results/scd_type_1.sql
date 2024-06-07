DROP TABLE nnkhanh_schema.scd_type_1;

CREATE TABLE nnkhanh_schema.scd_type_1
(
    cust_id           VARCHAR,
    cust_nm           TEXT,
    birth_date        DATE,
    add_id            VARCHAR,
    opn_dt            DATE,
    end_dt            DATE,
    record_created_at DATE DEFAULT CURRENT_DATE,
    PRIMARY KEY (cust_id)
);

INSERT INTO nnkhanh_schema.scd_type_1 (cust_id, cust_nm, birth_date, add_id, opn_dt, end_dt)
SELECT cust_id, cust_nm, birth_date, add_id, opn_dt, end_dt
FROM ai4e_test.customer;

INSERT INTO nnkhanh_schema.scd_type_1 (cust_id, cust_nm, birth_date, add_id, opn_dt, end_dt, record_created_at)
SELECT cust_id, cust_nm, birth_date, add_id, opn_dt, end_dt, '2023-10-18'
FROM ai4e_test.customer_cdc_18
ON CONFLICT (cust_id) DO UPDATE SET cust_id           = EXCLUDED.cust_id,
                                    cust_nm           = EXCLUDED.cust_nm,
                                    birth_date        = EXCLUDED.birth_date,
                                    add_id            = EXCLUDED.add_id,
                                    opn_dt            = EXCLUDED.opn_dt,
                                    end_dt            = EXCLUDED.end_dt,
                                    record_created_at = '2023-10-18';

INSERT INTO nnkhanh_schema.scd_type_1 (cust_id, cust_nm, birth_date, add_id, opn_dt, end_dt, record_created_at)
SELECT cust_id, cust_nm, birth_date, add_id, opn_dt, end_dt, '2023-10-19'
FROM ai4e_test.customer_cdc_19
ON CONFLICT (cust_id) DO UPDATE SET cust_id           = EXCLUDED.cust_id,
                                    cust_nm           = EXCLUDED.cust_nm,
                                    birth_date        = EXCLUDED.birth_date,
                                    add_id            = EXCLUDED.add_id,
                                    opn_dt            = EXCLUDED.opn_dt,
                                    end_dt            = EXCLUDED.end_dt,
                                    record_created_at = '2023-10-19';