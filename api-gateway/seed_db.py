import requests
import json
import time

# Service URLs from within Docker network
CUSTOMER_SERVICE_URL = "http://customer-service:8000"
BOOK_SERVICE_URL = "http://book-service:8000"
CART_SERVICE_URL = "http://cart-service:8000"
ORDER_SERVICE_URL = "http://order-service:8000"

def post_data(service_url, endpoint, data):
    url = f"{service_url}/{endpoint}"
    print(f"POST {url}")
    try:
        r = requests.post(url, json=data, timeout=30)
        r.raise_for_status()
        print(f"Success: {r.json()}")
        return r.json()
    except requests.exceptions.HTTPError as e:
        print(f"Validation Error: {r.json()}")
        return r.json()
    except Exception as e:
        print(f"Error: {e}")
        return None

def seed():
    print("Seeding data...")

    # Wait for services to be ready
    time.sleep(10)

    # 1. Seed Books
    books = [
        {"title": "Dune", "author": "Frank Herbert", "price": 15.99, "stock": 100},
        {"title": "The Hobbit", "author": "J.R.R. Tolkien", "price": 12.50, "stock": 50},
        {"title": "Sherlock Holmes", "author": "Arthur Conan Doyle", "price": 10.00, "stock": 30},
        {"title": "A Brief History of Time", "author": "Stephen Hawking", "price": 20.00, "stock": 20},
        {"title": "The Alchemist", "author": "Paulo Coelho", "price": 14.00, "stock": 75}
    ]
    for book in books:
        res = post_data(BOOK_SERVICE_URL, "books/", book)

    # 2. Seed Customers
    customers = [
        {"name": "John Doe", "email": "john@example.com", "password": "password123"},
        {"name": "Jane Smith", "email": "jane@example.com", "password": "password123"},
        {"name": "Bob Johnson", "email": "bob@example.com", "password": "password123"}
    ]
    customer_ids = []
    for customer in customers:
        res = post_data(CUSTOMER_SERVICE_URL, "customers/", customer)
        if res and res.get("id"):
            customer_ids.append(res.get("id"))
        else:
            # Try to fetch existing customer by email
            try:
                r = requests.get(f"{CUSTOMER_SERVICE_URL}/customers/", timeout=10)
                if r.status_code == 200:
                    for existing in r.json():
                        if existing['email'] == customer['email']:
                            customer_ids.append(existing['id'])
                            break
            except Exception:
                pass

    # 3. Add books to cart
    if len(customer_ids) >= 2:
        cart_items = [
            {"customer_id": customer_ids[0], "book_id": 1, "quantity": 2},
            {"customer_id": customer_ids[1], "book_id": 2, "quantity": 1},
        ]
        for item in cart_items:
            # We can use the add_to_cart view in the gateway
            add_to_cart_url = f"http://api-gateway:8000/cart/add/{item['book_id']}/"
            try:
                requests.post(add_to_cart_url, data={"customer_id": item['customer_id']}, timeout=30)
            except Exception:
                pass # This view redirects, so we can ignore the response

    # 4. Seed Orders
    # Filter out None and ensure we have enough IDs
    customer_ids = [cid for cid in customer_ids if cid]
    if len(customer_ids) >= 2:
        orders = [
            {"customer_id": customer_ids[0], "total_amount": "31.98", "status": "Shipped"},
            {"customer_id": customer_ids[1], "total_amount": "12.50", "status": "Pending"}
        ]
        for order in orders:
            post_data(ORDER_SERVICE_URL, "orders/", order)

    print("Seeding complete!")

if __name__ == "__main__":
    seed()
