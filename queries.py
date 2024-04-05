queries = {
'q1': '''select l_returnflag, l_linestatus,
            sum(l_quantity) as sum_qty, sum(l_extendedprice) as sum_base_price,
            sum(l_extendedprice * (1 - l_discount)) as sum_disc_price,
            sum(l_extendedprice * (1 - l_discount) * (1 + l_tax)) as sum_charge,
            avg(l_quantity) as avg_qty, avg(l_extendedprice) as avg_price,
            avg(l_discount) as avg_disc, count(*) as count_order
        from lineitem
        where l_shipdate <= date ('1998-12-01', '-3 days')
        group by l_returnflag, l_linestatus
        order by l_returnflag, l_linestatus;''',

'q2': '''select s_acctbal, s_name, n_name, p_partkey, p_mfgr, s_address, s_phone, s_comment
        from part, supplier, partsupp, nation, region
        where p_partkey = ps_partkey
            and s_suppkey = ps_suppkey
            and p_size = 15
            and p_type like '%BRASS'
            and s_nationkey = n_nationkey
            and n_regionkey = r_regionkey
            and r_name = 'EUROPE'
            and ps_supplycost = (
            select min(ps_supplycost)
                from partsupp, supplier, nation, region
            where p_partkey = ps_partkey and s_suppkey = ps_suppkey
                and s_nationkey = n_nationkey and n_regionkey = r_regionkey and r_name = 'EUROPE')
        order by s_acctbal desc, n_name, s_name, p_partkey;''',
'q3':'''select l_orderkey, sum(l_extendedprice * (1 - l_discount)) as revenue,
            o_orderdate, o_shippriority
        from customer, orders, lineitem
        where c_mktsegment = 'MACHINERY' and c_custkey = o_custkey
            and l_orderkey = o_orderkey and o_orderdate < date ('1995-03-21') and l_shipdate > date ('1995-03-21')
        group by l_orderkey, o_orderdate, o_shippriority
        order by revenue desc, o_orderdate;''',
'q4':'''select
o_orderpriority,
count(*) as order_count
from
orders
where
o_orderdate >= date ('1996-03-01')
and o_orderdate < date ('1996-03-01', '+3 months')
and exists (
select
*
from
lineitem
where
l_orderkey = o_orderkey
and l_commitdate < l_receiptdate
)
group by
o_orderpriority
order by
o_orderpriority;''',
'q5':'''select n_name, sum(l_extendedprice * (1 - l_discount)) as revenue
        from customer, orders, lineitem, supplier, nation, region
        where c_custkey = o_custkey and l_orderkey = o_orderkey and l_suppkey = s_suppkey
            and c_nationkey = s_nationkey and s_nationkey = n_nationkey
            and n_regionkey = r_regionkey and r_name = 'EUROPE' 
            and o_orderdate >= date ('1997-01-01') 
            and o_orderdate < date ('1997-01-01', '+1 years')
        group by n_name
        order by revenue desc;''',
'q6': '''select sum(l_extendedprice * l_discount) as revenue
        from lineitem
        where l_shipdate >= date ('1997-01-01') and l_shipdate < date ('1997-01-01', '+1 years')
            and l_discount between 0.07 - 0.01 and 0.07 + 0.01
            and l_quantity < 24;''',
'q7':'''select supp_nation, cust_nation, l_year, sum(volume) as revenue
        from (
            select n1.n_name as supp_nation, n2.n_name as cust_nation, strftime('%Y',l_shipdate) as l_year,
                l_extendedprice * (1 - l_discount) as volume
            from supplier, lineitem, orders, customer, nation n1, nation n2
            where s_suppkey = l_suppkey and o_orderkey = l_orderkey
                and c_custkey = o_custkey and s_nationkey = n1.n_nationkey
                and c_nationkey = n2.n_nationkey and (
                (n1.n_name = 'PERU' and n2.n_name = 'IRAQ')
                or (n1.n_name = 'IRAQ' and n2.n_name = 'PERU'))
        and l_shipdate between date ('1995-01-01') and date
('1996-12-31')
) as shipping
group by
supp_nation,
cust_nation,
l_year
order by
supp_nation,
cust_nation,
l_year;''',
'q8':'''select
o_year,
sum(case
when nation = 'IRAQ' then volume
else 0
end) / sum(volume) as mkt_share
from
(
select
strftime('%Y',o_orderdate) as o_year,
l_extendedprice * (1 - l_discount) as volume,
n2.n_name as nation
from
part,
supplier,
lineitem,
orders,
customer,
nation n1,
nation n2,
region
where
p_partkey = l_partkey
and s_suppkey = l_suppkey
and l_orderkey = o_orderkey
and o_custkey = c_custkey
and c_nationkey = n1.n_nationkey
and n1.n_regionkey = r_regionkey
and r_name = 'MIDDLE EAST'
and s_nationkey = n2.n_nationkey
and o_orderdate between date ('1995-01-01') and date
('1996-12-31')
and p_type = 'STANDARD ANODIZED BRASS'
) as all_nations
group by
o_year
order by
o_year;''',
'q9':'''select
nation,
o_year,
sum(amount) as sum_profit
from
(
select
n_name as nation,
strftime('%Y',o_orderdate) as o_year,
l_extendedprice * (1 - l_discount) - ps_supplycost *
l_quantity as amount
from
part,
supplier,
lineitem,
partsupp,
orders,
nation
where
s_suppkey = l_suppkey
and ps_suppkey = l_suppkey
and ps_partkey = l_partkey
and p_partkey = l_partkey
and o_orderkey = l_orderkey
and s_nationkey = n_nationkey
and p_name like '%antique%'
) as profit
group by
nation,
o_year
order by
nation,
o_year desc;''',
'q10':'''select
c_custkey,
c_name,
sum(l_extendedprice * (1 - l_discount)) as revenue,
c_acctbal,
n_name,
c_address,
c_phone,
c_comment
from
customer,
orders,
lineitem,
nation
where
c_custkey = o_custkey
and l_orderkey = o_orderkey
and o_orderdate >= date ('1993-12-01')
and o_orderdate < date ('1993-12-01', '+3 months')
and l_returnflag = 'R'
and c_nationkey = n_nationkey
group by
c_custkey,
c_name,
c_acctbal,
c_phone,
n_name,
c_address,
c_comment
order by
revenue desc;''',
'q11':'''select
ps_partkey,
sum(ps_supplycost * ps_availqty) as value
from
partsupp,
supplier,
nation
where
ps_suppkey = s_suppkey
and s_nationkey = n_nationkey
and n_name = 'CHINA'
group by
ps_partkey having
sum(ps_supplycost * ps_availqty) > (
select
sum(ps_supplycost * ps_availqty) * 0.0001000000
from
partsupp,
supplier,
nation
where
ps_suppkey = s_suppkey
and s_nationkey = n_nationkey
and n_name = 'CHINA'
)
order by
value desc;''',
'q12': '''select
l_shipmode,
sum(case
when o_orderpriority = '1-URGENT'
or o_orderpriority = '2-HIGH'
then 1
else 0
end) as high_line_count,
sum(case
when o_orderpriority <> '1-URGENT'
and o_orderpriority <> '2-HIGH'
then 1
else 0
end) as low_line_count
from
orders,
lineitem
where
o_orderkey = l_orderkey
and l_shipmode in ('AIR', 'RAIL')
and l_commitdate < l_receiptdate
and l_shipdate < l_commitdate
and l_receiptdate >= date ('1994-01-01')
and l_receiptdate < date ('1994-01-01', '+1 years')
group by
l_shipmode
order by
l_shipmode;''',
'q13':'''select
c_orders.c_count,
count(*) as custdist
from
(
select
c_custkey,
count(o_orderkey) as c_count
from
customer left outer join orders on
c_custkey = o_custkey
and o_comment not like '%pending%requests%'
group by
c_custkey
) as c_orders
group by
c_orders.c_count
order by
custdist desc,
c_orders.c_count desc;''',
'q14':'''select
100.00 * sum(case
when p_type like 'PROMO%'
then l_extendedprice * (1 - l_discount)
else 0
end) / sum(l_extendedprice * (1 - l_discount)) as promo_revenue
from
lineitem,
part
where
l_partkey = p_partkey
and l_shipdate >= date ('1994-12-01')
and l_shipdate < date ('1994-12-01', '+1 months');''',
'q15':'''with
revenue0 as
(select
l_suppkey as supplier_no,
sum(l_extendedprice * (1 - l_discount)) as total_revenue
from
lineitem
where
l_shipdate >= date ('1995-06-01')
and l_shipdate < date ('1995-06-01', '+3 months')
group by
l_suppkey)
select
s_suppkey,
s_name,
s_address,
s_phone,
total_revenue
from
supplier,
revenue0
where
s_suppkey = supplier_no
and total_revenue = (
select
max(total_revenue)
from
revenue0
)
order by
s_suppkey;''',
'q16':'''select
p_brand,
p_type,
p_size,
count(distinct ps_suppkey) as supplier_cnt
from
partsupp,
part
where
p_partkey = ps_partkey
and p_brand <> 'Brand#15'
and p_type not like 'MEDIUM BURNISHED%'
and p_size in (39, 26, 18, 45, 19, 1, 3, 9)
and ps_suppkey not in (
select
s_suppkey
from
supplier
where
s_comment like '%Customer%Complaints%'
)
group by
p_brand,
p_type,
p_size
order by
supplier_cnt desc,
p_brand,
p_type,
p_size;''',
'q17':'''select
sum(l_extendedprice) / 7.0 as avg_yearly
from
lineitem,
part
where
p_partkey = l_partkey
and p_brand = 'Brand#52'
and p_container = 'JUMBO CAN'
and l_quantity < (
select
0.2 * avg(l_quantity)
from
lineitem
where
l_partkey = p_partkey
);''',
'q18':'''select
c_name,
c_custkey,
o_orderkey,
o_orderdate,
o_totalprice,
sum(l_quantity)
from
customer,
orders,
lineitem
where
o_orderkey in (
select
l_orderkey
from
lineitem
group by
l_orderkey having
sum(l_quantity) > 313
)
and c_custkey = o_custkey
and o_orderkey = l_orderkey
group by
c_name,
c_custkey,
o_orderkey,
o_orderdate,
o_totalprice
order by
o_totalprice desc,
o_orderdate;''',
'q19':'''select
sum(l_extendedprice* (1 - l_discount)) as revenue
from
lineitem,
part
where
(
p_partkey = l_partkey
and p_brand = 'Brand#43'
and p_container in ('SM CASE', 'SM BOX', 'SM PACK', 'SM PKG')
and l_quantity >= 3 and l_quantity <= 3 + 10
and p_size between 1 and 5
and l_shipmode in ('AIR', 'AIR REG')
and l_shipinstruct = 'DELIVER IN PERSON'
)
or
(
p_partkey = l_partkey
and p_brand = 'Brand#25'
and p_container in ('MED BAG', 'MED BOX', 'MED PKG', 'MED PACK')
and l_quantity >= 10 and l_quantity <= 10 + 10
and p_size between 1 and 10
and l_shipmode in ('AIR', 'AIR REG')
and l_shipinstruct = 'DELIVER IN PERSON'
)
or
(
p_partkey = l_partkey
and p_brand = 'Brand#24'
and p_container in ('LG CASE', 'LG BOX', 'LG PACK', 'LG PKG')
and l_quantity >= 22 and l_quantity <= 22 + 10
and p_size between 1 and 15
and l_shipmode in ('AIR', 'AIR REG')
and l_shipinstruct = 'DELIVER IN PERSON'
);''',
'q20':'''select
sum(l_extendedprice* (1 - l_discount)) as revenue
from
lineitem,
part
where
(
p_partkey = l_partkey
and p_brand = 'Brand#43'
and p_container in ('SM CASE', 'SM BOX', 'SM PACK', 'SM PKG')
and l_quantity >= 3 and l_quantity <= 3 + 10
and p_size between 1 and 5
and l_shipmode in ('AIR', 'AIR REG')
and l_shipinstruct = 'DELIVER IN PERSON'
)
or
(
p_partkey = l_partkey
and p_brand = 'Brand#25'
and p_container in ('MED BAG', 'MED BOX', 'MED PKG', 'MED PACK')
and l_quantity >= 10 and l_quantity <= 10 + 10
and p_size between 1 and 10
and l_shipmode in ('AIR', 'AIR REG')
and l_shipinstruct = 'DELIVER IN PERSON'
)
or
(
p_partkey = l_partkey
and p_brand = 'Brand#24'
and p_container in ('LG CASE', 'LG BOX', 'LG PACK', 'LG PKG')
and l_quantity >= 22 and l_quantity <= 22 + 10
and p_size between 1 and 15
and l_shipmode in ('AIR', 'AIR REG')
and l_shipinstruct = 'DELIVER IN PERSON'
);''',
'q21':'''select
s_name,
s_address
from
supplier,
nation
where
s_suppkey in (
select
ps_suppkey
from
partsupp
where
ps_partkey in (
select
p_partkey
from
part
where
p_name like 'lime%'
)
and ps_availqty > (
select
0.5 * sum(l_quantity)
from
lineitem
where
l_partkey = ps_partkey
and l_suppkey = ps_suppkey
and l_shipdate >= date ('1994-01-01')
and l_shipdate < date ('1994-01-01', '+1
years')
)
)
and s_nationkey = n_nationkey
and n_name = 'VIETNAM'
order by
s_name;''',
'q21':'''select
s_name,
count(*) as numwait
from
supplier,
lineitem l1,
orders,
nation
where
s_suppkey = l1.l_suppkey
and o_orderkey = l1.l_orderkey
and o_orderstatus = 'F'
and l1.l_receiptdate > l1.l_commitdate
and exists (
select
*
from
lineitem l2
where
l2.l_orderkey = l1.l_orderkey
and l2.l_suppkey <> l1.l_suppkey
)
and not exists (
select
*
from
lineitem l3
where
l3.l_orderkey = l1.l_orderkey
and l3.l_suppkey <> l1.l_suppkey
and l3.l_receiptdate > l3.l_commitdate
)
and s_nationkey = n_nationkey
and n_name = 'INDIA'
group by
s_name
order by
numwait desc,
s_name;''',
'q22':'''select
cntrycode,
count(*) as numcust,
sum(c_acctbal) as totacctbal
from
(
select
substr(c_phone, 1, 2) as cntrycode,
c_acctbal
from
customer
where
substr(c_phone, 1, 2) in
('41', '28', '39', '21', '24', '29', '44')
and c_acctbal > (
select
avg(c_acctbal)
from
customer
where
c_acctbal > 0.00
and substr(c_phone, 1, 2) in
('41', '28', '39', '21', '24',
'29', '44')
)
and not exists (
select
*
from
orders
where
o_custkey = c_custkey
)
) as custsale
group by
cntrycode
order by
cntrycode;
'''
}

queries2 = {
'q17_drop_view':'''
DROP VIEW newTable;''',
'q17_create_view':'''
create view newTable as

select
    l_extendedprice,
    l_quantity 

from

    lineitem

join

    part on part.p_partkey = lineitem.l_partkey

where

    part.p_brand = 'Brand#52'

    and part.p_container = 'JUMBO CAN';''', 

'q17_call':'''

select

    sum(l_extendedprice) / 7.0 as avg_yearly

from

    newTable

where

    l_quantity < (

        select

            0.2 * avg(l_quantity)

        from

            newTable

    );
''', 
'q22_v3':'''WITH customer_avg AS (
    SELECT
        AVG(C_acctbal) AS avg_acctbal
    FROM
        Customer
    WHERE
        C_acctbal > 0.00
        AND SUBSTR(C_phone, 1, 2) IN ('41', '28', '39', '21', '24', '29', '44')
), filtered_customers AS (
    SELECT
        SUBSTR(C_phone, 1, 2) AS cntrycode,
        C_acctbal
    FROM
        Customer
    LEFT JOIN Orders ON C_custkey = O_custkey
    WHERE
        SUBSTR(C_phone, 1, 2) IN ('41', '28', '39', '21', '24', '29', '44')
        AND C_acctbal > (SELECT avg_acctbal FROM customer_avg)
        AND O_custkey IS NULL
)
SELECT
    cntrycode,
    COUNT(*) AS numcust,
    SUM(C_acctbal) AS totacctbal
FROM
    filtered_customers
GROUP BY
    cntrycode
ORDER BY
    cntrycode;


'''
}

queries3 = {
'q22_V2': '''
select
         cntrycode,
         count(*) as numcust,
         sum(c_acctbal) as totacctbal
 from
         (
                 select
                         substr(c_phone, 1, 2) as cntrycode,
                         c_acctbal
                 from
                         customer
                 where
                         substr(c_phone, 1, 2) in
                                 ('41', '28', '39', '21', '24', '29', '44')
                         and c_acctbal > (
                                 select
                                         avg(c_acctbal)
                                 from
                                         customer
                                 where
                                         c_acctbal > 0.00
                                         and substr(c_phone, 1, 2) in
                                                 ('41', '28', '39', '21', '24', '29', '44')
                         )
                         and not exists (
                                 select
                                         1
                                 from
                                         orders
                                 where
                                         o_custkey = c_custkey
                         )
         ) as custsale
 group by
         cntrycode
 order by
         cntrycode;

'''
}

queries4 = {
    'q22_v4':'''SELECT
    substr(c_phone, 1, 2) as cntrycode,
    COUNT(*) as numcust,
    SUM(c_acctbal) as totacctbal
FROM
    customer
WHERE
    substr(c_phone, 1, 2) IN ('41', '28', '39', '21', '24', '29', '44')
    AND c_acctbal > (
        SELECT
            AVG(c_acctbal)
        FROM
            customer
        WHERE
            c_acctbal > 0.00
            AND substr(c_phone, 1, 2) IN ('41', '28', '39', '21', '24', '29', '44')
    )
    AND NOT EXISTS (
        SELECT
            1
        FROM
            orders
        WHERE
            o_custkey = c_custkey
    )
GROUP BY
    cntrycode
ORDER BY
    cntrycode;
''',
'q22_v3':'''WITH customer_avg AS (
    SELECT
        AVG(C_acctbal) AS avg_acctbal
    FROM
        Customer
    WHERE
        C_acctbal > 0.00
        AND SUBSTR(C_phone, 1, 2) IN ('41', '28', '39', '21', '24', '29', '44')
), filtered_customers AS (
    SELECT
        SUBSTR(C_phone, 1, 2) AS cntrycode,
        C_acctbal
    FROM
        Customer
    LEFT JOIN Orders ON C_custkey = O_custkey
    WHERE
        SUBSTR(C_phone, 1, 2) IN ('41', '28', '39', '21', '24', '29', '44')
        AND C_acctbal > (SELECT avg_acctbal FROM customer_avg)
        AND O_custkey IS NULL
)
SELECT
    cntrycode,
    COUNT(*) AS numcust,
    SUM(C_acctbal) AS totacctbal
FROM
    filtered_customers
GROUP BY
    cntrycode
ORDER BY
    cntrycode;


'''
}


def returnQueries():
    return queries

def returnQueries2():
    return queries2

def returnQueries3():
    return queries3

def returnQueries4():
    return queries4