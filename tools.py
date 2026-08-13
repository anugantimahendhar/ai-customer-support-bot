import sqlite3
from langchain_core.tools import tool

DB_NAME = "data/orders.db"


@tool
def get_order_status(order_id: str):
    """Get complete order details using the order ID."""

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM orders WHERE order_id = ?",
        (order_id,)
    )

    order = cursor.fetchone()

    if order is None:
        conn.close()
        return "Order not found."

    columns = [description[0] for description in cursor.description]

    order_details = dict(zip(columns, order))

    conn.close()

    return order_details


@tool
def cancel_order(order_id: str):
    """Cancel an order if it has not been shipped or delivered."""

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT status FROM orders WHERE order_id = ?",
        (order_id,)
    )

    order = cursor.fetchone()

    if order is None:
        conn.close()
        return "Order not found."

    status = order[0].lower()

    if status in ["shipped", "delivered", "cancelled"]:
        conn.close()
        return (
            f"Order {order_id} cannot be cancelled "
            f"because its current status is '{status}'."
        )

    cursor.execute(
        "UPDATE orders SET status = ? WHERE order_id = ?",
        ("Cancelled", order_id)
    )

    conn.commit()
    conn.close()

    return f"Order {order_id} has been cancelled successfully."


@tool
def return_order(order_id: str):
    """Request a return for a delivered order."""

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT status FROM orders WHERE order_id = ?",
        (order_id,)
    )

    order = cursor.fetchone()

    if order is None:
        conn.close()
        return "Order not found."

    status = order[0].lower()

    if status != "delivered":
        conn.close()
        return (
            f"Order {order_id} cannot be returned yet "
            f"because its current status is '{status}'."
        )

    cursor.execute(
        "UPDATE orders SET status = ? WHERE order_id = ?",
        ("Return Requested", order_id)
    )

    conn.commit()
    conn.close()

    return f"Return request created successfully for {order_id}."