import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
OUT = BASE / "visualisations"
OUT.mkdir(exist_ok=True)

customers = pd.read_csv(BASE/"data/customers.csv")
products = pd.read_csv(BASE/"data/products.csv")
orders = pd.read_csv(BASE/"data/orders.csv", parse_dates=["OrderDate"])

# Data quality checks
print("Missing values:")
print(orders.isna().sum())
print("\nDuplicate orders:", orders["OrderID"].duplicated().sum())

# Join tables
sales = orders.merge(customers, on="CustomerID", how="left").merge(products, on="ProductID", how="left")
sales["Revenue"] = sales["Quantity"] * sales["UnitPrice"] * (1-sales["Discount"])
sales["Cost"] = sales["Quantity"] * sales["UnitCost"]
sales["Profit"] = sales["Revenue"] - sales["Cost"]
sales["ProfitMargin"] = np.where(sales["Revenue"] != 0, sales["Profit"]/sales["Revenue"]*100, 0)

print("\nKPI SUMMARY")
print("Revenue: R{:,.2f}".format(sales["Revenue"].sum()))
print("Cost: R{:,.2f}".format(sales["Cost"].sum()))
print("Profit: R{:,.2f}".format(sales["Profit"].sum()))
print("Orders:", sales["OrderID"].nunique())
print("Customers:", sales["CustomerID"].nunique())
print("Profit margin: {:.2f}%".format(sales["Profit"].sum()/sales["Revenue"].sum()*100))

# Monthly trend
monthly = sales.groupby(sales["OrderDate"].dt.to_period("M"))["Revenue"].sum()
plt.figure(figsize=(10,5))
monthly.plot()
plt.title("Monthly Revenue")
plt.xlabel("Month"); plt.ylabel("Revenue (ZAR)")
plt.tight_layout(); plt.savefig(OUT/"monthly_revenue.png", dpi=150); plt.close()

# Category revenue
category = sales.groupby("Category")["Revenue"].sum().sort_values()
plt.figure(figsize=(9,5))
category.plot(kind="barh")
plt.title("Revenue by Product Category")
plt.xlabel("Revenue (ZAR)")
plt.tight_layout(); plt.savefig(OUT/"revenue_by_category.png", dpi=150); plt.close()

# Province profit
province = sales.groupby("Province")["Profit"].sum().sort_values()
plt.figure(figsize=(9,5))
province.plot(kind="barh")
plt.title("Profit by Province")
plt.xlabel("Profit (ZAR)")
plt.tight_layout(); plt.savefig(OUT/"profit_by_province.png", dpi=150); plt.close()

# RFM analysis
snapshot = sales["OrderDate"].max() + pd.Timedelta(days=1)
rfm = sales.groupby("CustomerID").agg(
    Recency=("OrderDate", lambda x: (snapshot-x.max()).days),
    Frequency=("OrderID","nunique"),
    Monetary=("Revenue","sum")
).reset_index()

rfm["R_Score"] = pd.qcut(rfm["Recency"].rank(method="first"),5,labels=[5,4,3,2,1]).astype(int)
rfm["F_Score"] = pd.qcut(rfm["Frequency"].rank(method="first"),5,labels=[1,2,3,4,5]).astype(int)
rfm["M_Score"] = pd.qcut(rfm["Monetary"].rank(method="first"),5,labels=[1,2,3,4,5]).astype(int)
rfm["RFM_Score"] = rfm["R_Score"] + rfm["F_Score"] + rfm["M_Score"]

def segment(x):
    if x >= 13: return "High Value"
    if x >= 10: return "Loyal"
    if x >= 7: return "Potential"
    return "At Risk"

rfm["Segment"] = rfm["RFM_Score"].apply(segment)
rfm.to_csv(OUT/"customer_rfm.csv", index=False)

print("\nRFM segments:")
print(rfm["Segment"].value_counts())

# Discount relationship
discount_summary = sales.groupby("Discount").agg(
    Revenue=("Revenue","sum"), Profit=("Profit","sum")
).reset_index()
discount_summary["ProfitMargin"] = discount_summary["Profit"]/discount_summary["Revenue"]*100
print("\nDiscount analysis:")
print(discount_summary)

# Export clean analytical dataset
sales.to_csv(OUT/"sales_analytical_dataset.csv", index=False)
