-- 1.	Trả về tổng số tiền đã thu cho từng customer theo từng tháng đối với thẻ DEBIT.
SELECT
    c.cust_id,
    DATE_TRUNC('month', ct.transaction_time) as transaction_month,
    SUM(ct.amount) as total_revenue
FROM 
    ai4e_test.card_transaction ct
JOIN 
    ai4e_test.card ca ON ct.card_id = ca.card_id
JOIN 
    ai4e_test.customer c ON ca.cust_id = c.cust_id
JOIN 
    ai4e_test.card_type ct_type ON ca.card_type = ct_type.type_id
WHERE 
    ct_type.type_nm = 'DEBIT'
GROUP BY 
    c.cust_id, 
    DATE_TRUNC('month', ct.transaction_time)
ORDER BY 
    c.cust_id, 
    transaction_month;

-- 2.	Trả về top 10 customers có tổng số amount THU và CHI lớn nhất từ trước đến nay đối với thẻ DEBIT.
WITH DebitTransactions AS (
    SELECT
        c.cust_id,
        SUM(CASE WHEN ct.amount > 0 THEN ct.amount ELSE 0 END) AS total_revenue,
        SUM(CASE WHEN ct.amount < 0 THEN ct.amount ELSE 0 END) AS total_expenditure
    FROM
        ai4e_test.card_transaction ct
    JOIN
        ai4e_test.card c ON ct.card_id = c.card_id
    JOIN
        ai4e_test.card_type ct_type ON c.card_type = ct_type.type_id
    WHERE
        ct_type.type_nm = 'DEBIT'
    GROUP BY
        c.cust_id
)

SELECT
    cust_id,
    total_revenue,
    total_expenditure,
    (total_revenue + total_expenditure) AS total_amount
FROM
    DebitTransactions
ORDER BY
    total_amount DESC
LIMIT 10;

-- 3.	Trả về tổng số tiền đã thanh toán (chi) theo từng tháng với từng customer.
SELECT
    c.cust_id,
    transaction_time,
    SUM(pt.amount) as total_expenditure
FROM
    ai4e_test.payment_transaction pt
JOIN
    ai4e_test.account a ON pt.acc_id = a.acc_id
JOIN
    ai4e_test.customer c ON a.cust_id = c.cust_id
GROUP BY
    c.cust_id,
   transaction_time
ORDER BY
    c.cust_id,
    transaction_time;

-- 4.	Trả về thông tin tổng số tiền thanh toán (chi) tháng trước đó và tháng hiện tại đối với từng customers trên thẻ DEBIT.
WITH DebitTransactions AS (
    SELECT
        c.cust_id,
        DATE_TRUNC('month', ct.transaction_time) AS transaction_month,
        SUM(ct.amount) AS total_expenditure
    FROM
        ai4e_test.card_transaction ct
    JOIN
        ai4e_test.card c ON ct.card_id = c.card_id
    JOIN
        ai4e_test.customer cust ON c.cust_id = cust.cust_id
    JOIN
        ai4e_test.card_type ct_type ON c.card_type = ct_type.type_id
    WHERE
        ct_type.type_nm = 'DEBIT'
    GROUP BY
        c.cust_id,
        DATE_TRUNC('month', ct.transaction_time)
)

SELECT
    dt.cust_id,
    dt.transaction_month,
    dt.total_expenditure,
    COALESCE(LAG(dt.total_expenditure) OVER (PARTITION BY dt.cust_id ORDER BY dt.transaction_month), 0) AS previous_month_expenditure,
    dt.total_expenditure AS current_month_expenditure
FROM
    DebitTransactions dt
ORDER BY
    dt.cust_id,
    dt.transaction_month;

-- 5.	Trả về luỹ kế số tiền đã thanh toán theo từng tháng của mỗi customer trên thẻ DEBIT.
WITH DebitTransactions AS (
    SELECT
        c.cust_id,
        DATE_TRUNC('month', ct.transaction_time) AS transaction_month,
        SUM(ct.amount) AS monthly_expenditure
    FROM
        ai4e_test.card_transaction ct
    JOIN
        ai4e_test.card c ON ct.card_id = c.card_id
    JOIN
        ai4e_test.customer cust ON c.cust_id = cust.cust_id
    JOIN
        ai4e_test.card_type ct_type ON c.card_type = ct_type.type_id
    WHERE
        ct_type.type_nm = 'DEBIT'
    GROUP BY
        c.cust_id,
        DATE_TRUNC('month', ct.transaction_time)
)

SELECT
    dt.cust_id,
    dt.transaction_month,
    dt.monthly_expenditure,
    SUM(dt.monthly_expenditure) OVER (PARTITION BY dt.cust_id ORDER BY dt.transaction_month) AS cumulative_expenditure
FROM
    DebitTransactions dt
ORDER BY
    dt.cust_id,
    dt.transaction_month;