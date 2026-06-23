from datetime import timedelta
from random import choice, randint, uniform

from faker import Faker
from sqlalchemy import text

from database import engine

fake = Faker()

categories = [
    "Electronics",
    "Books",
    "Fashion",
    "Sports",
    "Home",
    "Beauty"
]

TOTAL_PRODUCTS = 200000
BATCH_SIZE = 5000

with engine.begin() as conn:

    print("Deleting old products...")
    conn.execute(text("DELETE FROM products"))

    for start in range(0, TOTAL_PRODUCTS, BATCH_SIZE):

        batch = []

        for _ in range(BATCH_SIZE):

            created_at = fake.date_time_between(
                start_date="-2y",
                end_date="now"
            )

            updated_at = created_at + timedelta(
                days=randint(0, 30)
            )

            batch.append(
                {
                    "name": fake.word().title() + " Product",
                    "category": choice(categories),
                    "price": round(uniform(100, 10000), 2),
                    "created_at": created_at,
                    "updated_at": updated_at,
                }
            )

        conn.execute(
            text("""
                INSERT INTO products
                (name, category, price, created_at, updated_at)
                VALUES
                (:name, :category, :price, :created_at, :updated_at)
            """),
            batch
        )

        print(
            f"Inserted {start + BATCH_SIZE:,} / {TOTAL_PRODUCTS:,}"
        )

print("Done!")