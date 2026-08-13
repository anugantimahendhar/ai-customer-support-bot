from tools import (
    get_order_status,
    cancel_order,
    return_order
)


print("===================================")
print("      AI CUSTOMER SUPPORT")
print("===================================")

order_id = input("\nEnter your Order ID: ").strip()

# Check order
order = get_order_status.invoke({
    "order_id": order_id
})

print("\n-----------------------------------")
print("ORDER DETAILS")
print("-----------------------------------")

if order == "Order not found.":
    print(order)

else:

    for key, value in order.items():
        print(f"{key}: {value}")

    print("\n-----------------------------------")
    print("What would you like to do?")
    print("-----------------------------------")

    print("1. Check Order")
    print("2. Cancel Order")
    print("3. Return Order")
    print("4. Exit")

    choice = input("\nEnter your choice: ").strip()

    if choice == "1":

        order = get_order_status.invoke({
            "order_id": order_id
        })

        print("\nCurrent Order Details:")

        for key, value in order.items():
            print(f"{key}: {value}")

    elif choice == "2":

        result = cancel_order.invoke({
            "order_id": order_id
        })

        print("\nCancellation Result:")
        print(result)

    elif choice == "3":

        result = return_order.invoke({
            "order_id": order_id
        })

        print("\nReturn Result:")
        print(result)

    elif choice == "4":

        print("\nThank you for using AI Customer Support.")

    else:

        print("\nInvalid choice.")