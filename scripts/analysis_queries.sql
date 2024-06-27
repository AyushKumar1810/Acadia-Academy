-- analysis_queries.sql

-- 1. What % of sales result in a return?
SELECT 
    (COUNT(DISTINCT r.sale_id) * 100.0 / COUNT(DISTINCT s.sale_id)) AS return_percentage
FROM 
    Sales s
LEFT JOIN 
    Returns r ON s.sale_id = r.sale_id;

-- 2. What % of returns are full returns?
SELECT 
    (COUNT(*) * 100.0 / (SELECT COUNT(*) FROM Returns)) AS full_return_percentage
FROM 
    Returns
WHERE 
    return_amount = sale_amount;

-- 3. What is the average return % amount (return % of original sale)?
SELECT 
    AVG(return_amount * 100.0 / sale_amount) AS average_return_percentage
FROM 
    Returns;

-- 4. What % of returns occur within 7 days of the original sale?
SELECT 
    (COUNT(*) * 100.0 / (SELECT COUNT(*) FROM Returns)) AS returns_within_7_days_percentage
FROM 
    Returns r
JOIN 
    Sales s ON r.sale_id = s.sale_id
WHERE 
    julianday(r.return_date) - julianday(s.sale_date) <= 7;

-- 5. What is the average number of days for a return to occur?
SELECT 
    AVG(julianday(r.return_date) - julianday(s.sale_date)) AS average_days_for_return
FROM 
    Returns r
JOIN 
    Sales s ON r.sale_id = s.sale_id;

-- 6. Who is our most valuable customer?
SELECT 
    s.customer_id, 
    SUM(s.sale_amount) - IFNULL(SUM(r.return_amount), 0) AS net_sales
FROM 
    Sales s
LEFT JOIN 
    Returns r ON s.sale_id = r.sale_id
GROUP BY 
    s.customer_id
ORDER BY 
    net_sales DESC
LIMIT 1;