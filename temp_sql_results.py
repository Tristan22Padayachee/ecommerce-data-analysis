import sqlite3
import pandas as pd
from pathlib import Path

root = Path(r'c:\Users\charm\OneDrive\Desktop\E-Commerce Project, SQL,R,Python\ecommerce-data-analysis')
conn = sqlite3.connect(':memory:')
for name in ['customers', 'products', 'orders']:
    df = pd.read_csv(root / 'data' / f'{name}.csv')
    if name == 'orders':
        df['OrderDate'] = pd.to_datetime(df['OrderDate']).dt.strftime('%Y-%m-%d')
    df.to_sql(name, conn, index=False, if_exists='replace')

queries = [
    ("Overall KPIs", '''
        SELECT COUNT(DISTINCT o.OrderID) AS total_orders,
               COUNT(DISTINCT o.CustomerID) AS unique_customers,
               ROUND(SUM(o.Quantity * p.UnitPrice * (1-o.Discount)), 2) AS revenue,
               ROUND(SUM(o.Quantity * p.UnitCost), 2) AS cost,
               ROUND(SUM((o.Quantity*p.UnitPrice*(1-o.Discount))-(o.Quantity*p.UnitCost)), 2) AS profit
        FROM orders o JOIN products p ON o.ProductID=p.ProductID;
    '''),
    ("Monthly revenue and profit", '''
        SELECT strftime('%Y-%m', o.OrderDate) AS month,
               ROUND(SUM(o.Quantity * p.UnitPrice * (1-o.Discount)), 2) AS revenue,
               ROUND(SUM((o.Quantity*p.UnitPrice*(1-o.Discount))-(o.Quantity*p.UnitCost)), 2) AS profit
        FROM orders o JOIN products p ON o.ProductID=p.ProductID
        GROUP BY 1 ORDER BY 1;
    '''),
    ("Category performance", '''
        SELECT p.Category,
               ROUND(SUM(o.Quantity*p.UnitPrice*(1-o.Discount)), 2) AS revenue,
               ROUND(SUM((o.Quantity*p.UnitPrice*(1-o.Discount))-(o.Quantity*p.UnitCost)), 2) AS profit,
               ROUND(100.0 * SUM((o.Quantity*p.UnitPrice*(1-o.Discount))-(o.Quantity*p.UnitCost)) / NULLIF(SUM(o.Quantity*p.UnitPrice*(1-o.Discount)),0), 2) AS profit_margin_pct
        FROM orders o JOIN products p ON o.ProductID=p.ProductID
        GROUP BY p.Category ORDER BY profit DESC;
    '''),
    ("Top 10 products", '''
        SELECT p.ProductName,p.Category,
               SUM(o.Quantity) AS units_sold,
               ROUND(SUM(o.Quantity*p.UnitPrice*(1-o.Discount)), 2) AS revenue
        FROM orders o JOIN products p ON o.ProductID=p.ProductID
        GROUP BY p.ProductID,p.ProductName,p.Category
        ORDER BY revenue DESC LIMIT 10;
    '''),
    ("Revenue by province", '''
        SELECT c.Province,
               ROUND(SUM(o.Quantity*p.UnitPrice*(1-o.Discount)), 2) AS revenue,
               ROUND(SUM((o.Quantity*p.UnitPrice*(1-o.Discount))-(o.Quantity*p.UnitCost)), 2) AS profit
        FROM orders o JOIN customers c ON o.CustomerID=c.CustomerID
        JOIN products p ON o.ProductID=p.ProductID
        GROUP BY c.Province ORDER BY revenue DESC;
    '''),
    ("Payment method performance", '''
        SELECT PaymentMethod, COUNT(*) AS orders,
               ROUND(SUM(o.Quantity*p.UnitPrice*(1-o.Discount)), 2) AS revenue
        FROM orders o JOIN products p ON o.ProductID=p.ProductID
        GROUP BY PaymentMethod ORDER BY revenue DESC;
    '''),
    ("Repeat customers", '''
        SELECT COUNT(*) AS repeat_customers
        FROM (
            SELECT CustomerID FROM orders
            GROUP BY CustomerID HAVING COUNT(DISTINCT OrderID)>1
        ) x;
    '''),
    ("Customer value", '''
        SELECT c.CustomerID,c.FirstName,c.LastName,
               COUNT(DISTINCT o.OrderID) AS orders,
               ROUND(SUM(o.Quantity*p.UnitPrice*(1-o.Discount)), 2) AS revenue
        FROM customers c
        JOIN orders o ON c.CustomerID=o.CustomerID
        JOIN products p ON o.ProductID=p.ProductID
        GROUP BY c.CustomerID,c.FirstName,c.LastName
        ORDER BY revenue DESC LIMIT 20;
    '''),
    ("Discount vs profit", '''
        SELECT Discount,
               ROUND(SUM(o.Quantity*p.UnitPrice*(1-o.Discount)), 2) AS revenue,
               ROUND(SUM((o.Quantity*p.UnitPrice*(1-o.Discount))-(o.Quantity*p.UnitCost)), 2) AS profit
        FROM orders o JOIN products p ON o.ProductID=p.ProductID
        GROUP BY Discount ORDER BY Discount;
    '''),
    ("Average order value", '''
        SELECT ROUND(AVG(order_value), 2) AS average_order_value
        FROM (
            SELECT o.OrderID,
                   SUM(o.Quantity*p.UnitPrice*(1-o.Discount)) AS order_value
            FROM orders o JOIN products p ON o.ProductID=p.ProductID
            GROUP BY o.OrderID
        ) x;
    '''),
]
for title, query in queries:
    print(f'\n=== {title} ===')
    rows = conn.execute(query).fetchall()
    cols = [d[0] for d in conn.execute(query).description]
    print(pd.DataFrame(rows, columns=cols).to_string(index=False))
