"""Generate the synthetic raw datasets used in the Hands-On Data Lab.

The data is SYNTHETIC (created with a fixed random seed) and deliberately
contains data-quality problems (missing values, duplicates, inconsistent text,
wrong data types, invalid values) so that the cleaning exercises are realistic.

Run from the project root:  python src/generate_data.py
"""
from pathlib import Path

import numpy as np
import pandas as pd

SEED = 42
rng = np.random.default_rng(SEED)
RAW = Path(__file__).resolve().parents[1] / "data" / "raw"
RAW.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------- products
catalog = {
    "Electronics": [("Wireless Mouse", 899), ("Bluetooth Speaker", 2499), ("Smartphone", 18999),
                    ("Laptop", 54999), ("Headphones", 3499), ("Smart Watch", 7999)],
    "Furniture": [("Office Chair", 6999), ("Study Desk", 8499), ("Bookshelf", 4599), ("Floor Lamp", 1899)],
    "Stationery": [("Notebook Pack", 249), ("Gel Pens (10)", 199), ("Desk Organizer", 549),
                   ("Planner", 399), ("Marker Set", 299)],
    "Clothing": [("T-Shirt", 599), ("Jeans", 1799), ("Hoodie", 1499), ("Sneakers", 2999), ("Jacket", 3499)],
}
rows, pid = [], 1
for cat, items in catalog.items():
    for name, price in items:
        rows.append({"product_id": f"P{pid:02d}", "product_name": name, "category": cat, "unit_price": price})
        pid += 1
products = pd.DataFrame(rows)

# --------------------------------------------------------------- customers
city_region = {"Hyderabad": "South", "Bengaluru": "South", "Chennai": "South", "Mumbai": "West",
               "Pune": "West", "Delhi": "North", "Jaipur": "North", "Kolkata": "East", "Bhubaneswar": "East"}
cities = list(city_region)
n_cust = 120
cust = pd.DataFrame({
    "customer_id": [f"C{i:03d}" for i in range(1, n_cust + 1)],
    "city": rng.choice(cities, n_cust, p=[.16, .16, .11, .14, .09, .14, .06, .09, .05]),
    "segment": rng.choice(["Consumer", "Corporate", "Home Office"], n_cust, p=[.55, .25, .20]),
    "age": rng.integers(19, 64, n_cust).astype(float),
})
cust["region"] = cust["city"].map(city_region)
signup = pd.to_datetime("2023-01-01") + pd.to_timedelta(rng.integers(0, 900, n_cust), unit="D")
cust["signup_date"] = signup.strftime("%Y-%m-%d")

# --- inject data-quality problems into customers
cust.loc[rng.choice(n_cust, 9, replace=False), "age"] = np.nan                      # missing ages
idx = rng.choice(n_cust, 10, replace=False)
cust.loc[idx[:5], "city"] = cust.loc[idx[:5], "city"].str.lower() + " "             # 'hyderabad '
cust.loc[idx[5:], "city"] = cust.loc[idx[5:], "city"].str.upper()                   # 'DELHI'
is_blr = (cust["city"] == "Bengaluru").to_numpy()
cust.loc[is_blr, "city"] = rng.choice(["Bengaluru", "Bangalore"], is_blr.sum())     # two names, one city
cust.loc[rng.choice(n_cust, 2, replace=False), "age"] = [260.0, -5.0]               # impossible ages

# ------------------------------------------------------------------ orders
n = 520
month_w = np.array([.07, .06, .07, .07, .08, .07, .07, .08, .08, .09, .13, .13])
month_w = month_w / month_w.sum()
months = rng.choice(np.arange(1, 13), n, p=month_w)
days = rng.integers(1, 28, n)
dates = pd.to_datetime({"year": 2025, "month": months, "day": days})
orders = pd.DataFrame({
    "order_id": [f"ORD{i:04d}" for i in range(1, n + 1)],
    "order_date": dates.dt.strftime("%Y-%m-%d"),
    "customer_id": rng.choice(cust["customer_id"], n),
    "product_id": rng.choice(products["product_id"], n),
})
helper = (orders.merge(products, on="product_id", how="left")
                .merge(cust[["customer_id", "region"]], on="customer_id", how="left"))
qty_max = {"Electronics": 2, "Furniture": 2, "Stationery": 8, "Clothing": 4}
orders["quantity"] = [int(rng.integers(1, qty_max[c] + 1)) for c in helper["category"]]
disc = rng.choice([0, 5, 10, 15, 20], n, p=[.35, .2, .2, .15, .10])
orders["discount_pct"] = [f"{d}%" for d in disc]
orders["payment_method"] = rng.choice(["Credit Card", "Debit Card", "UPI", "Cash"], n, p=[.28, .22, .38, .12])
orders["order_status"] = rng.choice(["Delivered", "Returned", "Cancelled"], n, p=[.89, .07, .04])
base = helper["region"].map({"South": 4.0, "West": 4.5, "North": 5.5, "East": 6.2}).to_numpy()
orders["delivery_days"] = np.clip(np.round(rng.normal(base, 1.1)), 1, None).astype(float)
rating = 4.9 - 0.32 * (orders["delivery_days"] - 4) + rng.normal(0, 0.6, n)
orders["rating"] = np.clip(np.round(rating), 1, 5).astype(float)


def pick(k):
    return rng.choice(n, k, replace=False)


# --- inject data-quality problems into orders
orders.loc[pick(26), "quantity"] = np.nan                    # missing quantity
orders.loc[pick(4), "quantity"] = [-1, -2, 0, 0]             # invalid quantity
orders.loc[pick(30), "rating"] = np.nan                      # customers who did not rate
orders.loc[pick(3), "rating"] = [0, 9, 7]                    # impossible ratings
orders.loc[pick(18), "delivery_days"] = np.nan               # missing delivery time
orders.loc[pick(3), "delivery_days"] = [60, 75, 90]          # extreme outliers
orders["delivery_days"] = orders["delivery_days"].astype(object)
orders.loc[pick(6), "delivery_days"] = "TBD"                 # text inside a numeric column
orders.loc[pick(15), "discount_pct"] = np.nan                # missing discount
orders.loc[pick(5), "discount_pct"] = "unknown"
orders.loc[pick(3), "order_date"] = ["2025-13-45", "not available", "2025-02-30"]   # invalid dates
pm = orders["payment_method"].copy()
i = pick(40)
pm.iloc[i[:14]] = pm.iloc[i[:14]].str.lower()
pm.iloc[i[14:26]] = pm.iloc[i[14:26]].str.upper()
pm.iloc[i[26:]] = " " + pm.iloc[i[26:]] + " "
orders["payment_method"] = pm
st = orders["order_status"].copy()
j = pick(20)
st.iloc[j[:10]] = st.iloc[j[:10]].str.lower()
st.iloc[j[10:]] = st.iloc[j[10:]] + " "
orders["order_status"] = st
orders.loc[pick(7), "customer_id"] = "C999"                  # customer missing from the customer table
dups = orders.sample(16, random_state=SEED)                  # exact duplicate rows
orders = pd.concat([orders, dups], ignore_index=True).sample(frac=1, random_state=SEED).reset_index(drop=True)

orders.to_csv(RAW / "orders.csv", index=False)
cust.to_csv(RAW / "customers.csv", index=False)
products.to_csv(RAW / "products.csv", index=False)
print("orders", orders.shape, "| customers", cust.shape, "| products", products.shape)
