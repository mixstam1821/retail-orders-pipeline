"""
Generates synthetic e-commerce data: customers, products, orders.
Output: CSVs in ./sample_data/
"""
import csv
import random
from datetime import datetime, timedelta
from pathlib import Path

from faker import Faker

fake = Faker()
random.seed(42)
Faker.seed(42)

OUT_DIR = Path(__file__).resolve().parent.parent / "sample_data"
OUT_DIR.mkdir(exist_ok=True)

N_CUSTOMERS = 200
N_PRODUCTS = 40
N_ORDERS = 2000

CATEGORIES = ["Electronics", "Home & Kitchen", "Books", "Sports", "Clothing", "Toys"]
ORDER_STATUSES = ["completed", "completed", "completed", "cancelled", "returned"]  # weighted


def generate_customers():
    rows = []
    for i in range(1, N_CUSTOMERS + 1):
        rows.append({
            "customer_id": i,
            "name": fake.name(),
            "email": fake.email(),
            "country": fake.country(),
            "signup_date": fake.date_between(start_date="-3y", end_date="-30d").isoformat(),
        })
    return rows


def generate_products():
    rows = []
    for i in range(1, N_PRODUCTS + 1):
        rows.append({
            "product_id": i,
            "product_name": fake.unique.catch_phrase(),
            "category": random.choice(CATEGORIES),
            "price": round(random.uniform(5, 500), 2),
        })
    return rows


def generate_orders(customers, products):
    rows = []
    start = datetime.now() - timedelta(days=180)
    for i in range(1, N_ORDERS + 1):
        order_date = start + timedelta(days=random.randint(0, 180), hours=random.randint(0, 23))
        customer = random.choice(customers)
        product = random.choice(products)
        rows.append({
            "order_id": i,
            "customer_id": customer["customer_id"],
            "product_id": product["product_id"],
            "order_date": order_date.strftime("%Y-%m-%d %H:%M:%S"),
            "quantity": random.randint(1, 5),
            "order_status": random.choice(ORDER_STATUSES),
        })
    return rows


def write_csv(path, rows, fieldnames):
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {len(rows)} rows -> {path}")


def main():
    customers = generate_customers()
    products = generate_products()
    orders = generate_orders(customers, products)

    write_csv(OUT_DIR / "customers.csv", customers,
              ["customer_id", "name", "email", "country", "signup_date"])
    write_csv(OUT_DIR / "products.csv", products,
              ["product_id", "product_name", "category", "price"])
    write_csv(OUT_DIR / "orders.csv", orders,
              ["order_id", "customer_id", "product_id", "order_date", "quantity", "order_status"])


if __name__ == "__main__":
    main()
