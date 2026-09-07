-- Business Analysis Queries
-- SQLite-compatible SQL

-- 1. Overall KPIs
SELECT
    COUNT(DISTINCT o.OrderID) AS total_orders,
    COUNT(DISTINCT o.CustomerID) AS unique_customers,
    SUM(o.Quantity * p.UnitPrice * (1-o.Discount)) AS revenue,
    SUM(o.Quantity * p.UnitCost) AS cost,
    SUM((o.Quantity*p.UnitPrice*(1-o.Discount))-(o.Quantity*p.UnitCost)) AS profit
FROM orders o JOIN products p ON o.ProductID=p.ProductID;

-- 2. Monthly revenue and profit
SELECT strftime('%Y-%m',o.OrderDate) AS month,
       SUM(o.Quantity*p.UnitPrice*(1-o.Discount)) AS revenue,
       SUM((o.Quantity*p.UnitPrice*(1-o.Discount))-(o.Quantity*p.UnitCost)) AS profit
FROM orders o JOIN products p ON o.ProductID=p.ProductID
GROUP BY 1 ORDER BY 1;

-- 3. Category performance
SELECT p.Category,
       SUM(o.Quantity*p.UnitPrice*(1-o.Discount)) AS revenue,
       SUM((o.Quantity*p.UnitPrice*(1-o.Discount))-(o.Quantity*p.UnitCost)) AS profit,
       ROUND(100.0*SUM((o.Quantity*p.UnitPrice*(1-o.Discount))-(o.Quantity*p.UnitCost))
             /NULLIF(SUM(o.Quantity*p.UnitPrice*(1-o.Discount)),0),2) AS profit_margin_pct
FROM orders o JOIN products p ON o.ProductID=p.ProductID
GROUP BY p.Category ORDER BY profit DESC;

-- 4. Top 10 products
SELECT p.ProductName,p.Category,
       SUM(o.Quantity) AS units_sold,
       SUM(o.Quantity*p.UnitPrice*(1-o.Discount)) AS revenue
FROM orders o JOIN products p ON o.ProductID=p.ProductID
GROUP BY p.ProductID,p.ProductName,p.Category
ORDER BY revenue DESC LIMIT 10;

-- 5. Revenue by province
SELECT c.Province,
       SUM(o.Quantity*p.UnitPrice*(1-o.Discount)) AS revenue,
       SUM((o.Quantity*p.UnitPrice*(1-o.Discount))-(o.Quantity*p.UnitCost)) AS profit
FROM orders o JOIN customers c ON o.CustomerID=c.CustomerID
JOIN products p ON o.ProductID=p.ProductID
GROUP BY c.Province ORDER BY revenue DESC;

-- 6. Payment method performance
SELECT PaymentMethod, COUNT(*) AS orders,
       SUM(o.Quantity*p.UnitPrice*(1-o.Discount)) AS revenue
FROM orders o JOIN products p ON o.ProductID=p.ProductID
GROUP BY PaymentMethod ORDER BY revenue DESC;

-- 7. Repeat customers
SELECT COUNT(*) AS repeat_customers
FROM (
    SELECT CustomerID FROM orders
    GROUP BY CustomerID HAVING COUNT(DISTINCT OrderID)>1
) x;

-- 8. Customer value
SELECT c.CustomerID,c.FirstName,c.LastName,
       COUNT(DISTINCT o.OrderID) AS orders,
       SUM(o.Quantity*p.UnitPrice*(1-o.Discount)) AS revenue
FROM customers c
JOIN orders o ON c.CustomerID=o.CustomerID
JOIN products p ON o.ProductID=p.ProductID
GROUP BY c.CustomerID,c.FirstName,c.LastName
ORDER BY revenue DESC LIMIT 20;

-- 9. Discount vs profit
SELECT Discount,
       SUM(o.Quantity*p.UnitPrice*(1-o.Discount)) AS revenue,
       SUM((o.Quantity*p.UnitPrice*(1-o.Discount))-(o.Quantity*p.UnitCost)) AS profit
FROM orders o JOIN products p ON o.ProductID=p.ProductID
GROUP BY Discount ORDER BY Discount;

-- 10. Average order value
SELECT AVG(order_value) AS average_order_value
FROM (
    SELECT o.OrderID,
           SUM(o.Quantity*p.UnitPrice*(1-o.Discount)) AS order_value
    FROM orders o JOIN products p ON o.ProductID=p.ProductID
    GROUP BY o.OrderID
) x;
