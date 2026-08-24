# E-Commerce Sales & Customer Analytics

## Project Overview
An end-to-end data analytics portfolio project using **SQL, Python and R** to analyse an e-commerce business. The project covers data modelling, data cleaning, exploratory analysis, customer segmentation, business intelligence and statistical modelling.

## Business Problem
Management wants to understand:
- sales and profit trends
- product/category performance
- regional performance
- customer value and retention
- the relationship between discounts and profitability

## Tech Stack
- SQL (PostgreSQL-compatible)
- Python (Pandas, NumPy, Matplotlib)
- R (tidyverse, ggplot2, lubridate)
- CSV
- Git/GitHub

## Project Structure
```text
data/                  Raw datasets
sql/                   Database schema and business queries
python/                Cleaning, EDA and RFM analysis
R/                     Statistical analysis and visualisation
visualisations/        Generated charts and analytical datasets
```

## Workflow
1. Load raw customer, product and order data.
2. Validate missing values and duplicate records.
3. Join the relational datasets.
4. Calculate revenue, cost, profit and margin.
5. Analyse sales trends and product performance with SQL and Python.
6. Segment customers using RFM analysis.
7. Test the relationship between discounts and profit using R.
8. Translate findings into business recommendations.

## Key Metrics
- Total Revenue
- Total Cost
- Total Profit
- Profit Margin
- Number of Orders
- Unique Customers
- Average Order Value
- Repeat Customer Rate
- Customer RFM Segments

## How to Run

### Python
```bash
pip install -r requirements.txt
python python/ecommerce_analysis.py
```

### R
Install packages:
```r
install.packages(c("tidyverse","lubridate"))
```

Then run:
```r
source("R/statistical_analysis.R")
```

### SQL
Create the three tables using `sql/database_schema.sql`, import the CSV files, then execute `sql/business_analysis.sql`.

## Portfolio Highlights
This project demonstrates:
- relational database querying
- SQL joins and aggregations
- data cleaning
- exploratory data analysis
- KPI development
- customer segmentation
- statistical correlation and regression
- data visualisation
- business storytelling

## Business Recommendations
After running the analysis, management can use the results to identify high-value customers, focus on profitable product categories, optimise discounting, and prioritise high-performing regions.

## Author
Tristan Padayachee
