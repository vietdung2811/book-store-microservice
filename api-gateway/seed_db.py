import requests
import json
import time

# Service URLs from within Docker network
CUSTOMER_SERVICE_URL = "http://customer-service:8000"
BOOK_SERVICE_URL = "http://book-service:8000"
CART_SERVICE_URL = "http://cart-service:8000"
STAFF_SERVICE_URL = "http://staff-service:8000"
MANAGER_SERVICE_URL = "http://manager-service:8000"
CATALOG_SERVICE_URL = "http://catalog-service:8000"
ORDER_SERVICE_URL = "http://order-service:8000"

def post_data(service_url, endpoint, data):
    url = f"{service_url}/{endpoint}"
    print(f"POST {url}")
    try:
        r = requests.post(url, json=data, timeout=30)
        r.raise_for_status()
        print(f"Success: {r.json()}")
        return r.json()
    except Exception as e:
        print(f"Error: {e}")
        return None

def seed():
    print("Seeding data...")

    # Wait for services to be ready
    time.sleep(10)

    # 1. Seed Categories
    categories = [
        {"name": "Science Fiction", "description": "Books about futuristic science and technology."},
        {"name": "Fantasy", "description": "Books featuring magical elements and mythical creatures."},
        {"name": "Mystery", "description": "Books focused on solving crimes or puzzles."},
        {"name": "Non-Fiction", "description": "Educational and real-world books."}
    ]
    for category in categories:
        post_data(CATALOG_SERVICE_URL, "categories/", category)

    # 2. Seed Books
    books = [
        {"title": "Dune", "author": "Frank Herbert", "price": 15.99, "stock": 100},
        {"title": "The Hobbit", "author": "J.R.R. Tolkien", "price": 12.50, "stock": 50},
        {"title": "Sherlock Holmes", "author": "Arthur Conan Doyle", "price": 10.00, "stock": 30},
        {"title": "A Brief History of Time", "author": "Stephen Hawking", "price": 20.00, "stock": 20},
        {"title": "The Alchemist", "author": "Paulo Coelho", "price": 14.00, "stock": 75}
    ]
    for book in books:
        res = post_data(BOOK_SERVICE_URL, "books/", book)

    # 3. Seed Customers
    customers = [
        {"name": "John Doe", "email": "john@example.com"},
        {"name": "Jane Smith", "email": "jane@example.com"},
        {"name": "Bob Johnson", "email": "bob@example.com"}
    ]
    customer_ids = []
    for customer in customers:
        res = post_data(CUSTOMER_SERVICE_URL, "customers/", customer)
        if res:
            customer_ids.append(res.get("id"))
            
    # 4. Seed Staff
    staff = [
        {"name": "Alice", "role": "Cashier", "email": "alice@example.com"},
        {"name": "Charlie", "role": "Stocker", "email": "charlie@example.com"},
    ]
    for s in staff:
        post_data(STAFF_SERVICE_URL, "staff/", s)

    # 5. Seed Manager
    managers = [
        {"name": "Eve", "department": "Sales", "email": "eve@example.com"},
        {"name": "Mallory", "department": "Inventory", "email": "mallory@example.com"},
    ]
    for m in managers:
        post_data(MANAGER_SERVICE_URL, "managers/", m)

    # 6. Add books to cart
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

    # 7. Seed Orders
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
