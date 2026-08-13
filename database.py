import sqlite3
import os

DB_NAME = "data/orders.db"


def get_connection():
    os.makedirs("data", exist_ok=True)
    return sqlite3.connect(DB_NAME)


def create_database():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            order_id TEXT PRIMARY KEY,
            customer_id TEXT,
            product TEXT,
            status TEXT,
            tracking_number TEXT,
            estimated_delivery TEXT
        )
    """)

    orders = [
        (
            "ORD1001",
            "CUST001",
            "iPhone Case",
            "Out for Delivery",
            "TRK123",
            "2026-08-12"
        ),
        (
            "ORD1002",
            "CUST002",
            "Running Shoes",
            "Shipped",
            "TRK456",
            "2026-08-14"
        ),
        (
            "ORD1003",
            "CUST003",
            "Headphones",
            "Delivered",
            "TRK789",
            "2026-08-09"
        )
    ]

    cursor.executemany("""
        INSERT OR IGNORE INTO orders
        VALUES (?, ?, ?, ?, ?, ?)
    """, orders)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    create_database()
    print("Database created successfully.")