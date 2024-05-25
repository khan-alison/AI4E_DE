select *
from ai4e_test.einvoice;

select invoiceno, sum(quantity) as total_quantity
from ai4e_test.einvoice
group by invoiceno
limit 10;

-- window function
select row_number() over (
    partition by invoiceno
    order by revenue desc
    ) as stt,
       *
from ai4e_test.einvoice e
limit 10;

--window function & aggregate function
-- kiểm tra từng customer doanh thu của tháng trước đó
with cte as (select customerid, invoicemonth, sum(revenue) as mothly_revenue
             from ai4e_test.einvoice
             group by customerid, invoicemonth
             order by customerid, invoicemonth)

select *,
       lag(mothly_revenue, 1) over (
           partition by customerid
           order by invoicemonth desc
           ) as next_month_revenue
from cte;


