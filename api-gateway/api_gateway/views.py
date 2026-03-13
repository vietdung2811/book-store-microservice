from django.shortcuts import render, redirect
import requests

BOOK_SERVICE_URL = "http://book-service:8000"
CART_SERVICE_URL = "http://cart-service:8000"
ORDER_SERVICE_URL = "http://order-service:8000"
STAFF_SERVICE_URL = "http://staff-service:8000"

def book_list(request):
    try:
        r = requests.get(f"{BOOK_SERVICE_URL}/books/", timeout=10)
        r.raise_for_status()
        books = r.json()
    except Exception as e:
        print(f"Error fetching books: {e}")
        books = []
    return render(request, "books.html", {"books": books})

def staff_manage_books(request):
    if request.method == "POST":
        data = {
            "title": request.POST.get("title"),
            "author": request.POST.get("author"),
            "price": request.POST.get("price"),
            "stock": request.POST.get("stock"),
        }
        try:
            requests.post(f"{BOOK_SERVICE_URL}/books/", json=data)
        except Exception:
            pass
        return redirect('staff_manage_books')
    
    try:
        r = requests.get(f"{BOOK_SERVICE_URL}/books/")
        books = r.json()
    except Exception:
        books = []
    return render(request, "manage_books.html", {"books": books})

def add_to_cart(request, book_id):
    customer_id = 1  # Default for demo
    if request.method == "POST":
        data = {
            "customer_id": customer_id,
            "book_id": book_id,
            "quantity": 1
        }
        try:
            requests.post(f"{CART_SERVICE_URL}/cart-items/", json=data, timeout=10)
        except Exception:
            pass
    return redirect('book_list')

def view_cart(request, customer_id):
    try:
        r = requests.get(f"{CART_SERVICE_URL}/carts/{customer_id}/", timeout=10)
        r.raise_for_status()
        cart_data = r.json()
        items = cart_data.get('items', [])
        total_price = sum(float(item['book']['price']) * item['quantity'] for item in items)
    except Exception:
        items = []
        total_price = 0
    return render(request, "cart.html", {"items": items, "total_price": total_price, "customer_id": customer_id})

def checkout(request, customer_id):
    if request.method == "POST":
        data = {
            "customer_id": customer_id,
            "total_amount": request.POST.get("total_amount"),
        }
        try:
            # Trigger order-service (which calls pay and ship services)
            requests.post(f"{ORDER_SERVICE_URL}/orders/", json=data, timeout=10)
        except Exception:
            pass
        return redirect('view_cart', customer_id=customer_id)
    return redirect('view_cart', customer_id=customer_id)
