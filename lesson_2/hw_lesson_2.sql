select *
from ai4e_test.einvoice;

-- 1, Trả về giá trị trung bình các đơn giá (unitprice), tổng số lượng (quantity)
-- mỗi đơn hàng (invoiceno) (distinct các bản ghi)
SELECT invoiceno,
       AVG(unitprice),
       SUM(quantity)
FROM ai4e_test.einvoice
GROUP BY invoiceno;

-- 2, Trả về giá trị trung bình các đơn giá (unitprice), tổng số lượng (quantity),
-- số lượng mặt hàng khác nhau trên mỗi đơn hàng (stockcode), đơn giá tối đa một mặt
-- hàng, đơn giá tối thiểu một mặt hàng cho mỗi đơn hàng
SELECT invoiceno,
       AVG(unitprice)            AS avg_unitprice,
       SUM(quantity)             AS total_quantity,
       COUNT(DISTINCT stockcode) AS distinct_stockcode_count,
       MIN(unitprice)            AS min_unitprice,
       MAX(unitprice)            AS max_unitprice
FROM ai4e_test.einvoice
GROUP BY invoiceno
;

-- 3. Trả về thứ hạng của các mặt hàng (stockcode) trong mỗi đơn hàng dựa theo sự GIẢM DẦN của đơn giá (unitprice)
SELECT invoiceno,
       stockcode,
       unitprice,
       RANK() OVER (PARTITION BY invoiceno ORDER BY unitprice DESC ) AS rank
FROM ai4e_test.einvoice
ORDER BY invoiceno, rank;

-- 4.	Trả về 5 mặt hàng cho mỗi đơn hàng có đơn giá cao nhất
-- SELECT e.invoiceno, e.stockcode
-- FROM ai4e_test.einvoice e
--          JOIN
--      (SELECT DISTINCT invoiceno,
--                       MAX(unitprice)
--       FROM ai4e_test.einvoice
--       GROUP BY invoiceno) subquery ON e.invoiceno = subquery.invoiceno
-- ;
WITH RankedItem AS (SELECT invoiceno,
                           stockcode,
                           unitprice,
                           RANK() OVER (PARTITION BY invoiceno ORDER BY unitprice DESC ) AS rank
                    FROM ai4e_test.einvoice
                    ORDER BY invoiceno, rank)
SELECT invoiceno,
       stockcode,
       unitprice,
       rank
FROM RankedItem
WHERE rank < 5
ORDER BY invoiceno, rank;


-- 5.	Trả về kết doanh thu tháng hiện tại, tháng trước đó và tháng tiếp theo mà mỗi khách hàng mang lại. (LEAD/LAG)
WITH cte AS (SELECT customerid, invoicemonth, sum(revenue) as monthly_revenue
             FROM ai4e_test.einvoice
             GROUP BY customerid, invoicemonth
             ORDER BY customerid, invoicemonth)
SELECT *,
       LAG(monthly_revenue, 1) OVER (PARTITION BY customerid ORDER BY invoicemonth DESC )  AS prev_month_revenue,
       LEAD(monthly_revenue, 1) OVER (PARTITION BY customerid ORDER BY invoicemonth DESC ) AS next_month_revenue
FROM cte

-- 6.	Tính luỹ kết doanh thu mỗi khách hàng mang lại theo từng tháng.
WITH cte AS (
    SELECT
        customerid,
        invoicemonth,
        SUM(revenue) AS monthly_revenue
    FROM
        ai4e_test.einvoice
    GROUP BY
        customerid,
        invoicemonth
    ORDER BY
        customerid,
        invoicemonth
)
SELECT
    customerid,
    invoicemonth,
    monthly_revenue,
    SUM(monthly_revenue) OVER (PARTITION BY customerid ORDER BY invoicemonth) AS cumulative_revenue
FROM
    cte
ORDER BY
    customerid,
    invoicemonth;