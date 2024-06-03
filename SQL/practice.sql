-- Bài tập 1: Tổng số tiền thu theo tháng cho từng khách hàng trên thẻ DEBIT
select cus.cust_id                             customer_id,
       to_char(ct.transaction_time, 'mm-yyyy') transaction_time,
       sum(ct.amount)                          monthly_transaction_amount
from ai4e_test.card_transaction ct
         join ai4e_test.card c on c.card_id = ct.card_id
         join ai4e_test.card_type ctype on ctype.type_id = c.card_type
         join ai4e_test.customer cus on cus.cust_id = c.cust_id
where ctype.type_nm = 'DEBIT'
  and ct.amount > 0
group by customer_id, transaction_time;

-- Bài tập 2: Số lần giao dịch và tổng số tiền chi theo loại thẻ
-- Yêu cầu: Viết câu truy vấn để trả về số lần giao dịch và tổng số tiền chi tiêu theo từng loại thẻ (chỉ các giao dịch có số tiền âm).
select ct.type_nm                     as card_type,
       count(card_transaction.amount) as number_of_transaction,
       sum(card_transaction.amount)   as total_spent_amount
from ai4e_test.card_transaction
         join ai4e_test.card c on c.card_id = card_transaction.card_id
         join ai4e_test.card_type ct on ct.type_id = c.card_type
where card_transaction.amount < 0
group by ct.type_nm;
-- Bài tập 3: Danh sách các khách hàng có giao dịch trong tháng gần nhất
-- Yêu cầu: Viết câu truy vấn để trả về danh sách các khách hàng có giao dịch trong tháng gần nhất (gần nhất so với thời điểm hiện tại).
with LatestMonth as (select date_trunc('month', max(transaction_time)) as latest_month from ai4e_test.card_transaction),
     TransactionInLatestMonth as (select c2.cust_id,
                                         c2.cust_nm,
                                         ct.transaction_time
                                  from ai4e_test.card_transaction ct
                                           join ai4e_test.card c on c.card_id = ct.card_id
                                           join ai4e_test.customer c2 on c2.cust_id = c.cust_id
                                           join LatestMonth
                                                on date_trunc('month', ct.transaction_time) = LatestMonth.latest_month)
select *
from TransactionInLatestMonth;

-- Bài tập 4: Tính tổng số dư cuối tháng của mỗi khách hàng
-- Yêu cầu: Viết câu truy vấn để tính tổng số dư cuối tháng của mỗi khách hàng dựa trên các giao dịch trong bảng card_transaction.
with TotalAmountTransaction as (select c.cust_id,
                                       date_trunc('month', ct.transaction_time) as transaction_month,
                                       sum(ct.amount)                           as total_amount
                                from ai4e_test.card_transaction ct
                                         join ai4e_test.card c on c.card_id = ct.card_id
                                         join ai4e_test.customer c2 on c2.cust_id = c.cust_id
                                group by c.cust_id, date_trunc('month', ct.transaction_time)),
     InitialBalance as (select c4.cust_id, min(ct.before_balance) as initial_balance
                        from ai4e_test.card_transaction ct
                                 join ai4e_test.card c3 on c3.card_id = ct.card_id
                                 join ai4e_test.customer c4 on c4.cust_id = c3.cust_id
                        group by c4.cust_id)

select total_amount.cust_id,
       total_amount.transaction_month,
       initial_balance.initial_balance,
       total_amount.total_amount,
       initial_balance.initial_balance + sum(total_amount.total_amount) over (
           partition by total_amount.cust_id order by total_amount.transaction_month
           ) as end_of_month_balance
from TotalAmountTransaction total_amount
         join InitialBalance initial_balance on total_amount.cust_id = initial_balance.cust_id
order by end_of_month_balance;

-- Bài tập 5: Tìm các khách hàng có chi tiêu trung bình hàng tháng lớn hơn một ngưỡng nhất định
-- Yêu cầu: Viết câu truy vấn để tìm các khách hàng có chi tiêu trung bình hàng tháng lớn hơn một ngưỡng nhất định (ví dụ: 1000).
with MonthlyTransaction as (select c.cust_id,
                                   date_trunc('month', ct.transaction_time) as transaction_month,
                                   sum(ct.amount)                           as total_amount
                            from ai4e_test.card_transaction ct
                                     join ai4e_test.card c on c.card_id = ct.card_id
                                     join ai4e_test.customer c2 on c2.cust_id = c.cust_id
                            group by c.cust_id, date_trunc('month', ct.transaction_time)),
     CustomerMontlyAvgTransaction as (select cust_id, avg(total_amount) avg_amount
                                      from MonthlyTransaction
                                      group by cust_id)
select cust_id, avg_amount
from CustomerMontlyAvgTransaction
where avg_amount > 1000
order by avg_amount desc;
-- Bài tập 6: Tìm các khách hàng có giao dịch nhiều nhất
-- Yêu cầu: Viết câu truy vấn để tìm các khách hàng có số lượng giao dịch nhiều nhất (chỉ tính các giao dịch từ thẻ DEBIT).
-- c1:
with TransactionTimes as (select c.cust_id as customer_id, count(trans_id) trans_times
                          from ai4e_test.card_transaction
                                   join ai4e_test.card c on c.card_id = card_transaction.card_id
                                   join ai4e_test.card_type ct on ct.type_id = c.card_type
                                   join ai4e_test.customer c2 on c2.cust_id = c.cust_id
                          where ct.type_nm = 'DEBIT'
                          group by c.cust_id)

select *
from TransactionTimes t
where trans_times = (select max(trans_times)
                     from TransactionTimes);

-- c2:
with RankingAvgAmount as (select c.cust_id,
                                 count(ct.trans_id)                              as trans_times,
                                 rank() over (order by count(ct.trans_id) desc ) as trans_rank
                          from ai4e_test.card_transaction ct
                                   join ai4e_test.card c on c.card_id = ct.card_id
                                   join ai4e_test.card_type t on t.type_id = c.card_type
                                   join ai4e_test.customer c2 on c2.cust_id = c.cust_id
                          where t.type_nm = 'DEBIT'
                          group by c.cust_id)
select cust_id, trans_times
from RankingAvgAmount
where trans_rank = 1;
-- Bài tập 7: Tổng chi tiêu theo ngày trong tuần
-- Yêu cầu: Viết câu truy vấn để tính tổng chi tiêu của khách hàng theo ngày trong tuần (ví dụ: tổng chi tiêu vào thứ Hai, thứ Ba, ...).
select to_char(ct.transaction_time, 'day') as day_of_week,
       sum(ct.amount)                      as total_spend_amount
from ai4e_test.card_transaction ct
         join ai4e_test.card c on c.card_id = ct.card_id
         join ai4e_test.customer c2 on c2.cust_id = c.cust_id
where ct.amount < 0
group by to_char(ct.transaction_time, 'day')
order by day_of_week;

-- Bài tập 8: Phân tích số dư trước và sau giao dịch
-- Yêu cầu: Viết câu truy vấn để phân tích số dư trước và sau mỗi giao dịch, tính tổng sự thay đổi số dư của từng khách hàng.
select c.cust_id, sum(payment_transaction.amount)
from ai4e_test.payment_transaction
         join ai4e_test.account a on a.acc_id = payment_transaction.acc_id
         join ai4e_test.customer c on c.cust_id = a.cust_id
group by c.cust_id;
-- Bài tập 9: Danh sách các giao dịch có giá trị lớn nhất trong mỗi tháng
-- Yêu cầu: Viết câu truy vấn để trả về danh sách các giao dịch có giá trị lớn nhất trong mỗi tháng (tính theo cả giá trị thu và chi).
with MonthlyTransaction as (select date_trunc('month', ct.transaction_time) as transaction_month,
                                   max(ct.amount)                           as total_amount
                            from ai4e_test.card_transaction ct
                            group by date_trunc('month', ct.transaction_time))
select ct.trans_id, ct.card_id, c2.cust_nm, ct.transaction_time, ct.amount
from ai4e_test.card_transaction ct
         join MonthlyTransaction mt
              on date_trunc('month', ct.transaction_time) = mt.transaction_month and ct.amount = mt.total_amount
         join ai4e_test.card c on c.card_id = ct.card_id
         join ai4e_test.customer c2 on c2.cust_id = c.cust_id;
-- Bài tập 10: Phân tích tỷ lệ giao dịch thành công và không thành công
-- Yêu cầu: Viết câu truy vấn để phân tích tỷ lệ giao dịch thành công và không thành công của từng khách hàng (giả sử bạn có cột status để xác định trạng thái của giao dịch).
-- Bài tập 11: Tính tổng số dư cuối ngày của mỗi khách hàng
-- Yêu cầu: Viết câu truy vấn để tính tổng số dư cuối ngày của mỗi khách hàng dựa trên các giao dịch trong bảng card_transaction.
with DailyBalance as (select c2.cust_id, date(ct.transaction_time) as transaction_date, ct.after_balance
                      from ai4e_test.card_transaction ct
                               join ai4e_test.card c on c.card_id = ct.card_id
                               join ai4e_test.customer c2 on c2.cust_id = c.cust_id)
select db.cust_id, transaction_date, max(db.after_balance)
from DailyBalance db
group by db.cust_id, transaction_date
order by db.cust_id, transaction_date;
-- Bài tập 12: Tìm các giao dịch có số tiền lớn hơn mức trung bình
-- Yêu cầu: Viết câu truy vấn để tìm các giao dịch có số tiền lớn hơn số tiền trung bình của tất cả các giao dịch trong bảng card_transaction.
with AvgAmountTransaction as (select avg(ct.amount) as avg_amount from ai4e_test.card_transaction ct)
select ct.trans_id, ct.amount, aat.avg_amount
from ai4e_test.card_transaction ct
         join AvgAmountTransaction aat on ct.amount > aat.avg_amount
-- Bài tập 13: Phân tích xu hướng chi tiêu theo giờ trong ngày
-- Yêu cầu: Viết câu truy vấn để phân tích tổng số tiền chi tiêu theo giờ trong ngày (ví dụ: từ 0 giờ đến 23 giờ) của từng khách hàng.
with TransactionInHour as (select c.cust_id,
                                  sum(ct.amount)                         as total_spent,
                                  extract(hour from ct.transaction_time) as transaction_hour
                           from ai4e_test.card_transaction ct
                                    join ai4e_test.card c on c.card_id = ct.card_id
                                    join ai4e_test.customer c2 on c2.cust_id = c.cust_id
                           where ct.amount < 0
                           group by c.cust_id, extract(hour from ct.transaction_time))
select sum(tih.total_spent), transaction_hour, cust_id
from TransactionInHour tih
where tih.transaction_hour > 9
  and tih.transaction_hour < 13
group by transaction_hour, cust_id
order by cust_id, transaction_hour;
-- Bài tập 14: Tìm khách hàng có sự thay đổi số dư lớn nhất
-- Yêu cầu: Viết câu truy vấn để tìm các khách hàng có sự thay đổi số dư lớn nhất (tính theo tổng sự thay đổi số dư của tất cả các giao dịch).
with BalanceAlternative as (select c.cust_id                                 as cus_id,
                                   sum(ct.after_balance - ct.before_balance) as total_balance_change
                            from ai4e_test.card_transaction ct
                                     join ai4e_test.card c on c.card_id = ct.card_id
                                     join ai4e_test.customer c2 on c2.cust_id = c.cust_id
                            group by c.cust_id)
select ba.cus_id, total_balance_change
from BalanceAlternative ba
order by total_balance_change desc
limit 1;

with BalanceAlternative as (
    select c.cust_id as cus_id, min(ct.amount) as min_amount, max(ct.amount) as max_amount
from ai4e_test.card_transaction ct
         join ai4e_test.card c on c.card_id = ct.card_id
         join ai4e_test.customer c2 on c2.cust_id = c.cust_id
group by c.cust_id
)
select ba.cus_id, (ba.max_amount - ba.min_amount) as difference from BalanceAlternative ba order by difference desc ;

-- Bài tập 15: Tính tổng số dư cuối tuần của mỗi khách hàng
-- Yêu cầu: Viết câu truy vấn để tính tổng số dư cuối tuần (Chủ nhật) của mỗi khách hàng dựa trên các giao dịch trong bảng card_transaction.
--
-- Bài tập 16: Phân tích số lượng giao dịch theo loại thẻ
-- Yêu cầu: Viết câu truy vấn để phân tích số lượng giao dịch theo loại thẻ (ví dụ: DEBIT, CREDIT).
--
-- Bài tập 17: Tính số dư trung bình hàng tháng của mỗi khách hàng
-- Yêu cầu: Viết câu truy vấn để tính số dư trung bình hàng tháng của mỗi khách hàng dựa trên các giao dịch trong bảng card_transaction.
--
-- Bài tập 18: Tìm các giao dịch có số tiền lớn nhất của từng khách hàng
-- Yêu cầu: Viết câu truy vấn để tìm các giao dịch có số tiền lớn nhất của từng khách hàng.
--
-- Bài tập 19: Phân tích số dư trước và sau giao dịch theo loại giao dịch
-- Yêu cầu: Viết câu truy vấn để phân tích số dư trước và sau giao dịch theo loại giao dịch (ví dụ: nạp tiền, rút tiền).
--
-- Bài tập 20: Tìm các khách hàng có số giao dịch bằng không trong tháng gần nhất
-- Yêu cầu: Viết câu truy vấn để tìm các khách hàng không có giao dịch nào trong tháng gần nhất.